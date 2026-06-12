/* Clanker City Chronicles — Scene 03: the Rustlers' alley. */

room AlleyRoom {

    // story flags (cross-room state rides on inventory ownership
    // instead — getObjectOwner(x) == VAR_EGO; NOT a bare truth test,
    // sld defaults owners to 0x0F — so these stay room-local)
    bit visitedAlley;
    bit metRivet;
    bit riddleDone;
    bit fareDone;

    object wayOut;
    object hideoutDoor;
    object graffiti;
    object dumpster;
    object fireEscape;
    object rivet;
    object junkHeap;
    object gate;
}
