#include <SerialTransfer.h>
#include <IRremote.hpp>

#define RED_PIN 3
#define GREEN_PIN 5
#define BLUE_PIN 6
#define IR_RECEIVER_PIN 11

#define LED_OFF 0
#define LED_ON_RED 1
#define LED_BLINKING_RED 2
#define LED_BLINKING_BLUE 3
#define LED_BLINKING_GREEN 4  
#define LED_ON_BLUE 5
#define LED_ON_GREEN 6
#define LED_ON_WHITE 7

//0 -> off, 1 -> Red, 2 -> blinking red (paused all), 3 -> blue blinking(audio on),4 -> green blinking (video on),5 -> only audio,6 -> only video 7 -> white (funny effect)

struct __attribute__((packed)) TX_STRUCT {
    unsigned int data;
} send_stat;

struct __attribute__((packed)) RX_STRUCT {
  char led_status;
} get_stat;


SerialTransfer pyTrans;

bool is_paused = false;
bool led_blinking = false;
bool combined_led_mode = false;
short last_mode = LED_OFF;

void setup() {
  Serial.begin(9600);
  pyTrans.begin(Serial);
  IrReceiver.begin(IR_RECEIVER_PIN, DISABLE_LED_FEEDBACK);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  analogWrite(RED_PIN, 0);    
  analogWrite(BLUE_PIN, 0);
  analogWrite(GREEN_PIN, 0);

 // send_stat.data = 0;
}

void loop() {

  if(IrReceiver.decode()){

      //if(send_stat.data != IrReceiver.decodedIRData.command){
      send_stat.data = IrReceiver.decodedIRData.command;      

      pyTrans.sendDatum(send_stat.data);

      IrReceiver.resume();
    }

    if(pyTrans.available()){
      
      pyTrans.rxObj(get_stat.led_status);
      
      led_blinking = change_led(get_stat.led_status);
    }
    
    if(led_blinking && (millis()%1000>500)){
      switch(is_paused){ //paused meaning led off
        case false:
          is_paused = change_led(get_stat.led_status);
          break;
        case true:
          is_paused = change_led(0);
          break;
      } 
      //maybe change this to lower
    }       
  }

bool change_led(int mode){

  bool should_blink = false;
  int colors[3] = {0,0,0};

  switch(mode){
    case LED_OFF:
          //for(int i = 0; i < 3; i++)
          //  colors[i] = 0;
          if(!led_blinking)
            combined_led_mode = false;
      break;
    case LED_ON_RED:
        colors[0] = 255;
        combined_led_mode = false;
      break;  
    case LED_BLINKING_RED:
          colors[0] = 255;
          should_blink = true;
          combined_led_mode = false;
      break;
      case LED_BLINKING_BLUE:
          if(last_mode == LED_BLINKING_GREEN || combined_led_mode){
            colors[0] = 255;
            combined_led_mode = true;
          }else
            colors[2] = 255;
          should_blink = true;
        break;
      case LED_BLINKING_GREEN:
          if(last_mode == LED_BLINKING_BLUE || combined_led_mode){
            colors[0] = 255;
            combined_led_mode = true;
          }else
            colors[1] = 255;
          should_blink = true;
        break;
      case LED_ON_BLUE:
       if(last_mode == LED_ON_GREEN){
            colors[0] = 255;
            mode = LED_ON_RED;
        }else
          colors[2] = 255;
        combined_led_mode = false;
        break;
      case LED_ON_GREEN:
       if(last_mode == LED_ON_BLUE){
            colors[0] = 255;
            mode = LED_ON_RED;
          }else
            colors[1] = 255;
          combined_led_mode = false;
        break;
      case LED_ON_WHITE:
         led_sound_state(last_mode);
        break;
      default:
        Serial.println("ERROR NO SUCH MODE"); //useless lol
  }

  analogWrite(RED_PIN, colors[0]);    
  analogWrite(GREEN_PIN, colors[1]);
  analogWrite(BLUE_PIN, colors[2]);
    
  if(last_mode != mode && (last_mode == LED_BLINKING_GREEN || last_mode == LED_BLINKING_BLUE) ||(last_mode == LED_ON_BLUE || last_mode == LED_ON_GREEN))
    last_mode = mode;
    
    //blue -> blinking, green -> blinking ==> red blinking, (last_mode = blue) mode = green, blue != green -> last_mode = mode both green -> off and green
  
  return should_blink;
}

void led_sound_state(short last_state){
  analogWrite(RED_PIN, 255);    
  analogWrite(GREEN_PIN, 255);
  analogWrite(BLUE_PIN, 255);
  delay(500);
  if(last_state != LED_ON_WHITE)
    change_led(last_state);
  else
    change_led(LED_OFF);
}
