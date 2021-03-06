import time

from pythonosc.udp_client import UDPClient

from .leap_python3 import Leap
from . import leap_utils
from . import osc_utils


class LeapListener(Leap.Listener):
    def on_init(self, controller):
        self.osc_client = UDPClient('127.0.0.1', 6448)

    def on_frame(self, controller):
        frame = controller.frame()
        positioning_values = leap_utils.get_raw_tip_positioning_data(frame)
        msg = osc_utils.build_osc_message(positioning_values)
        self.osc_client.send(msg)
        time.sleep(0.05)


def main():
    controller = Leap.Controller()
    listener = LeapListener()
    controller.add_listener(listener)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
