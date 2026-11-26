"""The game's sound beside other apps' on Android (AudioFocus.java with android/app/src/jvmtest's AudioFocusJvmTest): the game asks for no audio focus, so it plays
alongside a video in picture-in-picture or music instead of pausing it, and their playing never silences it; a phone call still interrupts the sound
(Native.audioInterrupt), through the audio mode. The JVM part is skipped without a JDK."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / 'android/app/src/main/java/dev/nxnative/android/AudioFocus.java'
TEST = REPO / 'android/app/src/jvmtest/java/dev/nxnative/android/AudioFocusJvmTest.java'
ACTIVITY = REPO / 'android/app/src/main/java/dev/nxnative/android/GameActivity.java'


class Wiring(unittest.TestCase):
    def test_activity_uses_it(self):
        t = ACTIVITY.read_text(encoding='utf-8')
        self.assertNotIn('requestAudioFocus', t)                                          # no focus: other apps' sound plays on beside the game
        self.assertIn('Native.audioInterrupt(AudioFocus.interrupts(m))', t)              # the mode listener goes through AudioFocus
        self.assertIn('addOnModeChangedListener(', t)
        self.assertIn('removeOnModeChangedListener(audioMode)', t)                       # and goes with the screen
        start = t[t.index('protected void onStart()'):t.index('protected void onResume()')]
        self.assertIn('AudioFocus.interrupts(audio.getMode())', start)                   # the return follows the mode as it is now
        self.assertLess(start.index('AudioFocus.interrupts(audio.getMode())'), start.index('Native.lifecycle(2)'))   # before the host resumes the sound

    def test_constants_match_android(self):
        # AudioManager.MODE_NORMAL / _RINGTONE / _IN_CALL / _IN_COMMUNICATION / _CALL_SCREENING / _CALL_REDIRECT / _COMMUNICATION_REDIRECT
        t = SRC.read_text(encoding='utf-8')
        self.assertIn('MODE_NORMAL = 0, MODE_RINGTONE = 1, MODE_IN_CALL = 2, MODE_IN_COMMUNICATION = 3, MODE_CALL_SCREENING = 4, MODE_CALL_REDIRECT = 5', t)
        self.assertIn('MODE_COMMUNICATION_REDIRECT = 6', t)


@unittest.skipUnless(shutil.which('javac') and shutil.which('java'), 'no JDK')
class AudioFocusJvm(unittest.TestCase):
    def test_jvm(self):
        with tempfile.TemporaryDirectory() as d:
            c = subprocess.run(['javac', '-Xlint:all', '-Werror', '-encoding', 'UTF-8', '-d', d, str(SRC), str(TEST)], capture_output=True, text=True)
            self.assertEqual(c.returncode, 0, c.stderr)
            r = subprocess.run(['java', '-cp', d, 'dev.nxnative.android.AudioFocusJvmTest'], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), 'ok')


if __name__ == '__main__':
    unittest.main()
