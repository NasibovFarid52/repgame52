from pygame import mixer
from constants import RAT_DEATH_SOUND, POLICEMAN_DEATH_SOUND, DOOR_ENTER_SOUND

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
        self.sound_volume = 0.5
        
    def load_sounds(self):
        self.sounds["rat_death"] = mixer.Sound(RAT_DEATH_SOUND)
        self.sounds["policeman_death"] = mixer.Sound(POLICEMAN_DEATH_SOUND)
        self.sounds["door_enter"] = mixer.Sound(DOOR_ENTER_SOUND)

    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sound_volume)
            self.sounds[sound_name].play()


    def set_volume(self, volume):
        self.sound_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)