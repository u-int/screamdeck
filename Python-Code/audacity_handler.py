import pyaudacity as pa

class AudacityHandler:
    
    is_paused = False
    is_recording = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AudacityHandler, cls).__new__(cls)
        return cls.instance


    def start_audio(self):
        if not self.is_recording and not self.is_paused:
            try:
                pa.record1st_choice()
                self.is_recording = True
            except pa.PyAudacityException:
                print('Start Audio failed, wrong params or argument')
        else:
            print('Cant Start recording!')

    def stop_audio(self):
        if self.is_recording or self.is_paused:
            try:
                pa.stop()
                self.is_recording = False
                self.is_paused = False
            except pa.PyAudacityException:
                print('Wrong argument or param, cant stop recording')
        else:
            print('Not recording nor paused!')

    def pause_audio(self):  
        
        if not self.is_paused:
            try:
                pa.pause()
                self.is_paused = True
            except pa.PyAudacityException:
                print('Cant be stopped or invalid argument.')
        else:
             print("Need to press continue button to unpause")

    def continue_audio(self):
        
        if self.is_paused:
            try: 
                pa.pause()
                self.is_paused = False
            except pa.PyAudacityException:
                print('Cant continue or invalid argument')
        else:
            print('You need to pause first!')

