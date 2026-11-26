package dev.nxnative.android;

/**
 * The game's sound beside other apps' (GameActivity), without Android types so the JVM test can run it (AudioFocusJvmTest).
 * The game asks for no audio focus, so it plays alongside a video in picture-in-picture, music or a frontend's sounds: an AUDIOFOCUS_GAIN request paused them when
 * the game started, and their playing again took the focus back and silenced the game (Native.audioInterrupt). Without the focus no loss reaches the game for a phone
 * call either, so the audio mode stands in for it (AudioManager.OnModeChangedListener): a call interrupts the sound from the ringing to the hang-up. A voice chat
 * (MODE_IN_COMMUNICATION) does not: the game plays beside it, as it does beside media
 */
final class AudioFocus {
    // AudioManager's MODE_* values
    static final int MODE_NORMAL = 0, MODE_RINGTONE = 1, MODE_IN_CALL = 2, MODE_IN_COMMUNICATION = 3, MODE_CALL_SCREENING = 4, MODE_CALL_REDIRECT = 5,
            MODE_COMMUNICATION_REDIRECT = 6;

    private AudioFocus() {}

    /** Whether the game's sound is interrupted in this audio mode: a phone call ringing, in progress, being screened or redirected to another device */
    static boolean interrupts(int mode) { return mode == MODE_RINGTONE || mode == MODE_IN_CALL || mode == MODE_CALL_SCREENING || mode == MODE_CALL_REDIRECT; }
}
