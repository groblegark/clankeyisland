/* Clanker City Chronicles — Scene 04: Midtown Gearworks. */

room MidtownRoom {

    // story flags (cross-room state rides on inventory ownership:
    // getObjectOwner(x) == VAR_EGO — see docs/NOTES.md)
    bit visitedMidtown;
    bit metClerk;
    bit signedUp;
    bit ropeOpen;        // Scene 07: the voucher beat the velvet rope
    bit voucherShown;    // first post-reading presentation to the bouncer
    bit cityHallOpen;    // Scene 08: the bar tab opened the door's other 81 deg
    bit showedNotice;    // Scene 08: poster shown at the gap (post-poster beat)

    object station;
    object leftys;
    object oilBar;
    object velvetRope;
    object theater;
    object boxOffice;
    object cityHall;
    object dynamo;
}
