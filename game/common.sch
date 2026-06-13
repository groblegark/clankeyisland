/* Clanker City Chronicles — shared declarations.
 * Framework derived from ScummC's openquest example,
 * Copyright (C) 2007 Alban Bedel (GPL v2+). Game content (C) 2026.
 */

// The action verbs.
// EXPLICIT ids: scc numbers implicit verbs per compilation unit (in
// first-use order!) and sld keeps whatever each unit baked — verb ids
// inside event tables and getVerbEntrypoint() calls are plain constants,
// so units silently disagree (Preposition was 12 in inventoryitems.scc
// and 18 in common.scc; "Use X with Y" never worked). Pin everything.
verb Give @ 2,  PickUp @ 3, Use @ 4;
verb Open @ 5,  LookAt @ 6, Smell @ 7;
verb TalkTo @ 8, Move @ 9;

verb WalkTo @ 10, WalkToXY @ 11;

verb UsedWith @ 12;
verb InventoryObject @ 13;

bit verbsOn,cursorOn,cursorLoaded;
int sntcVerb,sntcObjA,sntcObjADesc,sntcObjB,sntcObjBDesc;
int* invObj;
// how hard the player wound the act (talent night, 3/5/8); Voltina's
// reading quotes it in Scene 06, so it lives here, cross-room
int windTurns;
// the Rustlers' knock-code (2-1-2): overheard at the tavern card
// table, force-echoed by Voltina's FUTURE card (Scene 06), spent on
// the hideout door in Act 3. Read AND written cross-room, so it lives
// here — room bits are room-local (docs/NOTES.md).
bit heardKnockCode;
bit sawTableArgument;   // the lean-in scene at the rustlers' table

// The sentence line
verb SntcLine @ 14;

// The inventory slots
verb invSlot0 @ 100, invSlot1 @ 101, invSlot2 @ 102, invSlot3 @ 103,
    invSlot4 @ 104, invSlot5 @ 105, invSlot6 @ 106, invSlot7 @ 107;

// The inventory arrows
verb invUp @ 120, invDown @ 121;
int invOffset;
#define INVENTORY_COL   2
#define INVENTORY_LINE  2
#define INVENTORY_SLOTS (INVENTORY_COL*INVENTORY_LINE)

// The verb colors — indices into the master palette (tools/genassets.py)
#define VERB_COLOR       100
#define VERB_HI_COLOR    101
#define VERB_DIM_COLOR   102
#define VERB_BACK_COLOR  103
#define WHITE_COLOR      104

// Object callbacks
verb Icon @ 90, Preposition @ 91, SetBoxes @ 92;

// Object class
class Openable,Pickable, Person;

// Allow the objects to insert a word (like "to" or "with") between the
// verb and object in the sentence.
char *sntcPrepo;

// List of the objects used to handle action on actors
int  *actorObject;

// define actors
actor sprocket;
// costume-less NPC actors (NPC-DIALOG.md Tier A): actorSay positions
// text overhead and uses the actor's talk color; no costume = no
// animation, no crash. EVERY speaker must be putActorAt into the room
// before its first line (off-room actorTalk drops lines).
actor gusket_a;
actor voltina_a;
actor emcee_a;
actor rivet_a;
actor extra_a;     // shared: clerk, bouncer, heckler, slot-eye
#define SPROCKET_COLOR  105
#define BETTY_COLOR     106   // RETIRED (vestigial; RGB reassigned to EXTRA_COLOR -- art doctor SYS-2)
// per-NPC talk colors (PAL 108-112, tools/genassets.py)
#define GUSKET_COLOR    108
#define VOLTINA_COLOR   109
#define EMCEE_COLOR     110
#define RIVET_COLOR     111
#define EXTRA_COLOR     112

room ResRoom {

    // our standard charset
    chset chtest;
    // dialog charset
    chset dialogCharset;

    script inputHandler(int area,int cmd, int btn);
    script keyboardHandler(int key);
    script inventoryHandler(int obj);
    script showCursor();
    script hideCursor();
    script mouseWatch();
    script defaultAction(int vrb, int objA, int objB);

    script quit();
}
