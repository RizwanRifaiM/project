import time     
import sys
import tellopy
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font
import os
import datetime
import cev
from subprocess import Popen, PIPE
from djitellopy import Tello
import numpy as np

prev_flight_data = None
video_player = None
video_recorder = None
font = None
wid = None
date_fmt = '%Y-%m-%d_%H%M%S'

def process_tello_video(drone):
    while True:
        frame = drone.get_frame_read().frame
        cev.imshow("Frame", frame)
        if cev.waitKey(1) & 0xFF == ord('q'):
            break
    cev.destroyAllWindows()

def recording(drone):
    folder = "record_drone"
    nama_video = "videodrone.mp4"
    jenis = cev.VideoWriter_fourcc(*'mp4v')
    video_path = os.path.join(folder, nama_video)
    video = cev.VideoWriter(video_path, jenis, 30.0, (960, 720))

    while True:
        frame = drone.get_frame_read().frame
        frame = cev.cvtColor(frame, cev.COLOR_RGB2BGR)

        cev.imshow("Recording", frame)
        video.write(frame)

        key = cev.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    
    video.release()
    cev.destroyAllWindows()
    drone.streamoff()

def toggle_recording(drone, speed):
    global video_recorder
    global date_fmt
    if speed == 0:
        return

    if video_recorder:     
        # already recording, so stop
        video_recorder.release()
        status_print('Video saved to %s' % video_recorder.video_filename)
        video_recorder = None
        return

    # start a new recording
    filename = os.path.join('D:', 'python', 'videoDrone', f'tello-{datetime.datetime.now().strftime(date_fmt)}.mp4')

    fourcc = cev.VideoWriter_fourcc(*'mp4v')
    video_recorder = cev.VideoWriter(filename, fourcc, 30.0, (960, 720))
    video_recorder.video_filename = filename
    status_print('Recording video to %s' % filename)

def take_picture(drone, speed): 
    if speed == 0:
        return
    drone.take_picture()

def palm_land(drone, speed):
    if speed == 0:
        return
    drone.palm_land()

def toggle_zoom(drone, speed):
    if speed == 0:
        return
    drone.set_video_mode(not drone.zoom)
    pygame.display.get_surface().fill((0,0,0))
    pygame.display.flip()

def exit_program(drone, speed):
    drone.land()
    cev.destroyAllWindows()

controls = {
    'w': 'forward',
    's': 'backward',
    'a': 'left',
    'd': 'right',
    'space': 'up',
    'left shift': 'down',
    'right shift': 'down',
    'q': 'counter_clockwise',
    'e': 'clockwise',
    'left': lambda drone, speed: drone.counter_clockwise(speed*2),
    'right': lambda drone, speed: drone.clockwise(speed*2),
    'up': lambda drone, speed: drone.up(speed*2),
    'down': lambda drone, speed: drone.down(speed*2),
    'tab': lambda drone, speed: drone.takeoff(),
    'backspace': lambda drone, speed: drone.land(),
    'p': palm_land,
    'r': toggle_recording,
    'z': toggle_zoom,
    'enter': take_picture,
    'return': take_picture,
    'l': exit_program
}

class FlightDataDisplay(object):
    def __init__(self, key, format, colour=(255,255,255), update=None):
        self._key = key
        self._format = format
        self._colour = colour
        self._value = None
        self._surface = None

        if update:
            self._update = update
        else:
            self._update = lambda drone, data: getattr(data, self._key)

    def update(self, drone, data):
        new_value = self._update(drone, data)
        if self._value != new_value:
            self._value = new_value
            self._surface = font.render(self._format % (new_value,), True, self._colour)
        return self._surface

def flight_data_mode(drone, *args):
    return "VID" if drone.zoom else "PIC"

def flight_data_recording(*args):
    return "REC 00:00" if video_recorder else ""

def update_hud(hud, drone, flight_data):
    (w, h) = (158, 0)
    blits = []
    for element in hud:
        surface = element.update(drone, flight_data)
        if surface is None:
            continue
        blits += [(surface, (0, h))]
        h += surface.get_height()
    h += 64
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0,0,0))
    for blit in blits:
        overlay.blit(*blit)
    pygame.display.get_surface().blit(overlay, (0,0))
    pygame.display.update(overlay.get_rect())

def status_print(text):
    pygame.display.set_caption(text)

def start_stream():
    # Inisialisasi dan konfigurasi streaming video
    pass

class VideoStreamDisplay:
    def __init__(self, stream_function):
        self.stream_function = stream_function

    def display(self):
        # Logika untuk menampilkan video streaming di HUD
        self.stream_function()

video_display = VideoStreamDisplay(start_stream)

hud = [
    FlightDataDisplay('height', 'ALT %3d'),
    FlightDataDisplay('ground_speed', 'SPD %3d'),
    FlightDataDisplay('battery_percentage', 'BAT %3d%%'),
    FlightDataDisplay('wifi_strength', 'NET %3d%%'),
    FlightDataDisplay(None, 'CAM %s', update=flight_data_mode),
    FlightDataDisplay(None, '%s', colour=(255, 0, 0), update=flight_data_recording),
    video_display  # Menambahkan streaming video ke dalam HUD
]

def flightDataHandler(event, sender, data):
    global prev_flight_data
    text = str(data)
    if prev_flight_data != text:
        update_hud(hud, sender, data)
        prev_flight_data = text

def videoFrameHandler(event, sender, data):
    global video_player
    global video_recorder
    if video_player is None:
        cmd = ['mplayer', '-fps', '35', '-really-quiet']
        if wid is not None:
            cmd = cmd + ['-wid', str(wid)]
        video_player = Popen(cmd + ['-'], stdin=PIPE)

    try:
        video_player.stdin.write(data)
    except IOError as err:
        status_print(str(err))
        video_player = None

    try:
        if video_recorder:
            video_recorder.write(cev.imdecode(np.frombuffer(data, np.uint8), cev.IMREAD_COLOR))
    except IOError as err:
        status_print(str(err))
        video_recorder = None

def handleFileReceived(event, sender, data):
    global date_fmt
    path = os.path.join('D:', 'project', 'drone2', 'photos', f'tello-{datetime.datetime.now().strftime(date_fmt)}.jpeg')
    with open(path, 'wb') as fd:
        fd.write(data)
    status_print('Saved photo to %s' % path)

def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1280, 720))
    pygame.font.init()

    global font
    font = pygame.font.SysFont("dejavusansmono", 32)

    global wid
    if 'window' in pygame.display.get_wm_info():
        wid = pygame.display.get_wm_info()['window']
    print("Tello video WID:", wid)

    drone = Tello()
    drone.connect()
    drone.streamon()
    
    speed = 30

    try:
        while True:
            time.sleep(0.01)
            for e in pygame.event.get():
                if e.type == pygame.locals.KEYDOWN:
                    print('+' + pygame.key.name(e.key))
                    keyname = pygame.key.name(e.key)
                    if keyname == 'escape':
                        drone.land()
                        exit(0)
                    if keyname in controls:
                        key_handler = controls[keyname]
                        if isinstance(key_handler, str):
                            getattr(drone, key_handler)(speed)
                        else:
                            key_handler(drone, speed)

                elif e.type == pygame.locals.KEYUP:
                    print('-' + pygame.key.name(e.key))
                    keyname = pygame.key.name(e.key)
                    if keyname in controls:
                        key_handler = controls[keyname]
                        if isinstance(key_handler, str):
                            getattr(drone, key_handler)(0)
                        else:
                            key_handler(drone, 0)
    except Exception as e:
        print(str(e))
    finally:
        print('Shutting down connection to drone...')
        if video_recorder:
            toggle_recording(drone, 1)
        drone.land()
        drone.streamoff()
        exit(1)

if __name__ == '__main__':
    main()