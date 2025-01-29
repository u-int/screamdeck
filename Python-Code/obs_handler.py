import obsws_python as obsws

class ObsHandler:

    # Make class Singleton so it can only be created once
    def __new__(cls):
        if not hasattr(cls, 'instance'):                            
            cls.instance = super(ObsHandler, cls).__new__(cls)
        return cls.instance
    # Make a connection/request to the client (OBS)
    def __init__(self):
        self.ws = obsws.ReqClient()
        self.played_sound = False
    #Defining all the different Functions which make API-Calls/Requests to the OBS-Websocket
    def stop_video(self):
        try:
            self.ws.stop_record()
        except obsws.error.OBSSDKRequestError:
            print("Cant stop the video recording.")

    def pause_video(self):
        try:
            self.ws.pause_record()
        except obsws.error.OBSSDKRequestError:
            print("Cant pause the video recording.")
            
    def play_sound(self):
        try:
            if not self.played_sound:
                self.ws.trigger_media_input_action('WompWomp', 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY')
                self.played_sound = True
            elif self.played_sound:   
                self.ws.trigger_media_input_action('WompWomp', 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART')
        except obsws.error.OBSSDKRequestError:
            print("Cant play the sound.")
            
    def continue_video(self):
        try:
            self.ws.resume_record()        
        except obsws.error.OBSSDKRequestError:
            print("Cant continue the recording.")
            
    def start_recording(self):
        try:
            self.ws.start_record()
        except obsws.error.OBSSDKRequestError:
            print("Cant start the recording.")
    # After we are finished messing around, close the Web-Socket
    def end_routine(self):
        self.ws.disconnect()