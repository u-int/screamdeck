import time
from pySerialTransfer import pySerialTransfer as txfer
import obs_handler as obsh
import audacity_handler as pah

# Init variable for LED-Status
led_status = 0

# Dictionary for all the different commands delivered by the Arduino (IR-Sensor + Remote)
ir_signals = {
    22: "continue_all",#0
    12: "start_all",   #1 
    24: "stop_all",    #2
    94: "pause_all",   #3
    8: "start_audio",  #4
    28: "stop_audio",  #5
    90: "pause_audio", #6 
    66: "start_video", #7
    82: "stop_video",  #8
    74: "pause_video", #9 
    69: "funny_effect" #on
} 

if __name__ == '__main__':
    try:
        # Init all the API-Classes
        obs = obsh.ObsHandler()
        audacity = pah.AudacityHandler()
        # Establish a connection with the dedicated Device
        link = txfer.SerialTransfer('ttyACM0', baud=9600)
        openend = link.open()       
        print(openend)
        time.sleep(4.0)
        
        # Loop for reading and sending out messages to controll the LED-State/Make changes to the Video/Audio recordings
        while True:
            if link.available():
                rec_payload = link.rx_obj(obj_type='H', obj_byte_size=2)
                match rec_payload:
                    case 69: #funny sound
                        led_status = 7
                        print(ir_signals.get(69))
                        obs.play_sound()
                    case 12: #start all
                        led_status = 1
                        print(ir_signals.get(12))
                        obs.start_recording()
                        audacity.start_audio()
                    case 24: #stop all
                        led_status = 0
                        print(ir_signals.get(24))
                        obs.stop_video()
                        audacity.stop_audio()
                    case 94: #pause all
                        led_status = 2
                        print(ir_signals.get(94))
                        obs.pause_video()
                        audacity.pause_audio()
                    case 22: #continue all
                        led_status = 1          
                        print(ir_signals.get(22))
                        obs.continue_video()
                        audacity.continue_audio()
                    case 90: #pause audio
                        led_status = 3
                        print(ir_signals.get(90))
                        audacity.pause_audio()
                    case 74: #pause video
                        led_status = 4  
                        print(ir_signals.get(74))
                        obs.pause_video()
                    case 28: #stop audio
                        led_status = 6
                        print(ir_signals.get(28))
                        audacity.stop_audio()
                    case 82: #stop video
                        led_status = 5
                        print(ir_signals.get(82))
                        obs.stop_video()
                    case 8: #start audio
                        led_status = 5
                        print(ir_signals.get(8))
                        audacity.start_audio()
                    case 66: #start video
                        led_status = 6
                        print(ir_signals.get(66))
                        obs.start_recording()
                    case 0:
                        print("Received nothing")
                    case _:
                        print("nothing bound to this button.")
                # Init. and sending of message (LED)
                send_size = 0
                status_size = link.tx_obj(led_status)
                send_size += status_size
                link.send(send_size)

                while not link.available():
                    # Error-Stuff
                    if link.status <= 0:
                        match(link.status):
                            case txfer.Status.CRC_ERROR:
                                print('ERROR: CRC_ERROR')
                            case txfer.Status.PAYLOAD_ERROR:
                                print('ERROR: PAYLOAD_ERROR')
                            case txfer.Status.STOP_BYTE_ERROR:
                                print('ERROR: STOP_BYTE_ERROR')                 
                            case _:
                                print('ERROR: {}'.format(link.status))
    # Make sure to get out of the infinite Loop with a Interrupt (eg. CTRL+C)
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass

    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass
    