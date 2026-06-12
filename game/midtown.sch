/* Clanker City Chronicles — Scene 04: Midtown Gearworks. */

room MidtownRoom {

    // story flags (cross-room state rides on inventory ownership:
    // getObjectOwner(x) == VAR_EGO — see docs/NOTES.md)
    bit visitedMidtown;
    bit metClerk;
    bit signedUp;

    object station;
    object leftys;
    object oilBar;
    object theater;
    object boxOffice;
    object cityHall;
    object dynamo;
}
