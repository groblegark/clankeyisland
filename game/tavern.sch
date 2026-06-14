/* Clanker City Chronicles — Scene 02: the Scrap & Barrel tavern. */

room TavernRoom {

    // story flags
    bit visitedTavern;
    bit servoFixed;
    bit dartsDone;
    bit doorBackOpen;    // Scene 09: the hideout front door has been opened
    // heardKnockCode moved to common.sch (Scene 06 reads/writes it)

    object doorOut;
    object barSign;
    object shelf;
    object barCounter;
    object gusket;
    object piano;
    object rustlersTable;
    object dartboard;
    object flange;
    object doorBack;
}
