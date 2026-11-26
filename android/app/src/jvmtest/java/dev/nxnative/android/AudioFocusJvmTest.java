package dev.nxnative.android;

/** AudioFocus on the JVM (dm/tools/tests/test_android_audiofocus.py): which audio modes interrupt the game's sound. Prints "ok" or throws */
public final class AudioFocusJvmTest {
    private static void check(boolean c, String what) { if (!c) throw new AssertionError(what); }

    public static void main(String[] args) {
        // Media, a video in picture-in-picture, a notification: the mode stays normal, the game plays beside them
        check(!AudioFocus.interrupts(AudioFocus.MODE_NORMAL), "normal: the game plays");
        // A phone call, from the ringing to the hang-up
        check(AudioFocus.interrupts(AudioFocus.MODE_RINGTONE), "ringing interrupts");
        check(AudioFocus.interrupts(AudioFocus.MODE_IN_CALL), "a call interrupts");
        check(AudioFocus.interrupts(AudioFocus.MODE_CALL_SCREENING), "a screened call interrupts");
        check(AudioFocus.interrupts(AudioFocus.MODE_CALL_REDIRECT), "a call on another device interrupts");
        // A voice chat plays beside the game, as media does
        check(!AudioFocus.interrupts(AudioFocus.MODE_IN_COMMUNICATION), "voice chat: the game plays");
        check(!AudioFocus.interrupts(AudioFocus.MODE_COMMUNICATION_REDIRECT), "redirected voice chat: the game plays");
        check(!AudioFocus.interrupts(-2) && !AudioFocus.interrupts(-1) && !AudioFocus.interrupts(7), "an unknown or invalid mode does not interrupt");
        System.out.println("ok");
    }
}
