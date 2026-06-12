/* Clanker City Chronicles — Scene 06: backstage at the Grand Cog. */

room BackstageRoom {

    // story flags (cross-room state rides on inventory ownership or
    // common.sch globals — heardKnockCode/windTurns live THERE; these
    // stay room-local on purpose, see docs/NOTES.md)
    bit visitedBackstage;
    bit metVoltina;
    bit askedCrank;
    bit askedWant;
    bit knewKnock;

    object doorStage;
    object costumeRack;
    object ghostLight;
    object fuseBox;
    object voltina;
    object readingTable;
    object cardCarousel;
    object keyJar;
    object cables;
}
