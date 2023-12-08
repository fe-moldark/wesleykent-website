/*Adopted from original script here: https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards

To set this up yourself follow the steps outlined here - https://www.instructables.com/How-to-Make-a-USB-Laptop-Keyboard-Controller/
That guy does a terrific job at clearly outlining every step to get your keyboard working.

This script is designed for a Zenith Data Systems Z-note 433Lnp+.

The only function key that I programmed is Print Screen at F1. The rest are old functions that were used 30 years ago, but not anymore.

While the key matrix for this laptop model will work for anyone else with the same laptop, the Teensy I/O pins will no doubt be different
for you. Just follow the instructions from the link listed above to set this up yourself.

Using the Arduino IDE use the Teensy 4.0 as the board, Keyboard layout as US English, and USB Type as Keyboard.
*/


#define MODIFIERKEY_FN 0x8f   // Gives Fn key a fake HID code 
#define KEY_PAD_LOCK 0x8e     // Gives Pad Lock key a fake HID code
#define HEARTBEAT_LED 13      // LED ON Teensy set to blink

const byte rows_max = 11; // Num of rows in the keyboard matrix --> Outputs
const byte cols_max = 8;  // Num of columns in the keyboard matrix --> Inputs

// Load the normal key matrix with the Teensyduino key names described at www.pjrc.com/teensy/td_keyboard.html 
// A zero indicates no normal key at that location.
int normal[rows_max][cols_max] = {
  {KEY_X,KEY_CAPS_LOCK,KEY_Z,0,0,0,0,KEY_TAB},
  {KEY_M,KEY_SPACE,0,0,KEY_LEFT,0,KEY_DOWN,KEY_RIGHT},
  {KEY_T,KEY_Y,KEY_5,KEY_4,KEY_3,KEY_F2,KEY_F1,KEY_ESC},
  {KEY_J,KEY_U,KEY_8,KEY_7,KEY_6,KEY_F5,KEY_F4,KEY_F3},
  {KEY_H,KEY_G,KEY_F,KEY_R,KEY_E,KEY_W,KEY_2,KEY_1},
  {KEY_N,KEY_B,KEY_V,KEY_C,KEY_D,KEY_S,KEY_A,KEY_Q},
  {KEY_COMMA,KEY_PERIOD,KEY_SLASH,0,KEY_UP,0,0,0},
  {KEY_K,KEY_I,KEY_O,KEY_9,KEY_0,KEY_F6,KEY_F7,KEY_F8},
  {KEY_L,KEY_LEFT_BRACE,KEY_P,KEY_EQUAL,KEY_MINUS,KEY_F11,KEY_F10,KEY_F9},
  {KEY_SEMICOLON,KEY_QUOTE,KEY_RIGHT_BRACE,KEY_ENTER,KEY_BACKSPACE,KEY_F12,KEY_INSERT,KEY_DELETE},
  {0,KEY_END,KEY_TILDE,0,KEY_BACKSLASH,KEY_PAGE_DOWN,KEY_PAGE_UP,KEY_HOME}
};


// I am not using numlock, i.e. never defined - just make sure the right # of rows and cols are present
int numlock[rows_max][cols_max] = {
  {KEY_X,KEY_CAPS_LOCK,KEY_Z,MODIFIERKEY_LEFT_ALT,MODIFIERKEY_LEFT_SHIFT,MODIFIERKEY_FN,MODIFIERKEY_LEFT_CTRL,KEY_TAB},
  {KEY_M,KEY_SPACE,MODIFIERKEY_RIGHT_ALT,MODIFIERKEY_RIGHT_CTRL,KEY_LEFT,0,KEY_DOWN,KEY_RIGHT},
  {KEY_T,KEY_Y,KEY_5,KEY_4,KEY_3,KEY_F2,KEY_F1,KEY_ESC},
  {KEY_J,KEY_U,KEY_8,KEY_7,KEY_6,KEY_F5,KEY_F4,KEY_F3},
  {KEY_H,KEY_G,KEY_F,KEY_R,KEY_E,KEY_W,KEY_2,KEY_1},
  {KEY_N,KEY_B,KEY_V,KEY_C,KEY_D,KEY_S,KEY_A,KEY_Q},
  {KEY_COMMA,KEY_PERIOD,KEY_SLASH,MODIFIERKEY_RIGHT_SHIFT,KEY_UP,0,0,0},
  {KEY_K,KEY_I,KEY_O,KEY_9,KEY_0,KEY_F6,KEY_F7,KEY_F8},
  {KEY_L,KEY_LEFT_BRACE,KEY_P,KEY_EQUAL,KEY_MINUS,KEY_F11,KEY_F10,KEY_F9},
  {KEY_SEMICOLON,KEY_QUOTE,KEY_RIGHT_BRACE,KEY_ENTER,KEY_BACKSPACE,KEY_F12,KEY_INSERT,KEY_DELETE},
  {0,KEY_END,KEY_TILDE,0,KEY_BACKSLASH,KEY_PAGE_DOWN,KEY_PAGE_UP,KEY_HOME}
};

// I am not using padlock, i.e. never defined - just make sure the right # of rows and cols are present
int padlock[rows_max][cols_max] = {
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0}
};

// Load the modifier key matrix with key names at the correct row-column location. 
int modifier[rows_max][cols_max] = {
  {0,0,0,MODIFIERKEY_LEFT_ALT,MODIFIERKEY_LEFT_SHIFT,MODIFIERKEY_FN,MODIFIERKEY_LEFT_CTRL,0},
  {0,0,MODIFIERKEY_RIGHT_ALT,MODIFIERKEY_RIGHT_CTRL,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,MODIFIERKEY_RIGHT_SHIFT,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0}
};

// These are your Fn / function keys --> look to where the "actual" key is located in the matrix, copy over like below
// Only practical function key on this laptop was Print Screen by the way
int media[rows_max][cols_max] = {
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,KEY_PRINTSCREEN,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0}
};

// Initialize the old_key matrix with one's (nothing pressed). 
// 1 = key not pressed, 0 = key is pressed
boolean old_key[rows_max][cols_max] = {
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1},
  {1,1,1,1,1,1,1,1}
};

// Assign the Teensy I/O row numbers
int Row_IO[rows_max] = {1,2,3,4,5,6,7,8,9,10,11};

// Assign the column I/O numbers
int Col_IO[cols_max] = {21,20,19,18,17,16,15,14}; 

// declare keyboard variables
boolean slots_full = LOW; // Goes high when slots 1 thru 6 contain normal keys
// slot 1 thru slot 6 hold the normal key values to be sent over USB. 
int slot1 = 0; //value of 0 means the slot is empty and can be used.  
int slot2 = 0; 
int slot3 = 0; 
int slot4 = 0; 
int slot5 = 0; 
int slot6 = 0;
int mod_shift_l = 0;
int mod_shift_r = 0;
int mod_ctrl_l = 0;   
int mod_ctrl_r = 0;
int mod_alt_l = 0;
int mod_alt_r = 0;
int mod_gui = 0;

// Function to load the key name into the first available slot
void load_slot(int key) {
  if (!slot1)  {
    slot1 = key;
  }
  else if (!slot2) {
    slot2 = key;
  }
  else if (!slot3) {
    slot3 = key;
  }
  else if (!slot4) {
    slot4 = key;
  }
  else if (!slot5) {
    slot5 = key;
  }
  else if (!slot6) {
    slot6 = key;
  }
  if (!slot1 || !slot2 || !slot3 || !slot4 || !slot5 || !slot6)  {
    slots_full = LOW; // slots are not full
  }
  else {
    slots_full = HIGH; // slots are full
  } 
}

// Function to clear the slot that contains the key name
void clear_slot(int key) {
  if (slot1 == key) {
    slot1 = 0;
  }
  else if (slot2 == key) {
    slot2 = 0;
  }
  else if (slot3 == key) {
    slot3 = 0;
  }
  else if (slot4 == key) {
    slot4 = 0;
  }
  else if (slot5 == key) {
    slot5 = 0;
  }
  else if (slot6 == key) {
    slot6 = 0;
  }
  if (!slot1 || !slot2 || !slot3 || !slot4 || !slot5 || !slot6)  {
    slots_full = LOW;
  }
  else {
    slots_full = HIGH;
  } 
}

// Function to load the modifier key name into the appropriate mod variable
void load_mod(int m_key) {
  if (m_key == MODIFIERKEY_LEFT_SHIFT)  {
    mod_shift_l = m_key;
  }
  else if (m_key == MODIFIERKEY_RIGHT_SHIFT)  {
    mod_shift_r = m_key;
  }
  else if (m_key == MODIFIERKEY_LEFT_CTRL)  {
    mod_ctrl_l = m_key;
  }
  else if (m_key == MODIFIERKEY_RIGHT_CTRL)  {
    mod_ctrl_r = m_key;
  }
  else if (m_key == MODIFIERKEY_LEFT_ALT)  {
    mod_alt_l = m_key;
  }
  else if (m_key == MODIFIERKEY_RIGHT_ALT)  {
    mod_alt_r = m_key;
  }
  else if (m_key == MODIFIERKEY_GUI)  {
    mod_gui = m_key;
  }
}

// Function to load 0 into the appropriate mod variable
void clear_mod(int m_key) {
  if (m_key == MODIFIERKEY_LEFT_SHIFT)  {
    mod_shift_l = 0;
  }
  else if (m_key == MODIFIERKEY_RIGHT_SHIFT)  {
    mod_shift_r = 0;
  }
  else if (m_key == MODIFIERKEY_LEFT_CTRL)  {
    mod_ctrl_l = 0;
  }
  else if (m_key == MODIFIERKEY_RIGHT_CTRL)  {
    mod_ctrl_r = 0;
  }
  else if (m_key == MODIFIERKEY_LEFT_ALT)  {
    mod_alt_l = 0;
  }
  else if (m_key == MODIFIERKEY_RIGHT_ALT)  {
    mod_alt_r = 0;
  }
  else if (m_key == MODIFIERKEY_GUI)  {
    mod_gui = 0;
  }
}

// Function to send the modifier keys over usb
void send_mod() {
  Keyboard.set_modifier(mod_shift_l | mod_shift_r | mod_ctrl_l | mod_ctrl_r | mod_alt_l | mod_alt_r | mod_gui);
  Keyboard.send_now();
}

// Function to send the normal keys in the 6 slots over usb
void send_normals() {
  Keyboard.set_key1(slot1);
  Keyboard.set_key2(slot2);
  Keyboard.set_key3(slot3);
  Keyboard.set_key4(slot4);
  Keyboard.set_key5(slot5);
  Keyboard.set_key6(slot6);
  Keyboard.send_now();
}

// Function to set a pin to high impedance
void go_z(int pin)
{
  pinMode(pin, INPUT);
  digitalWrite(pin, HIGH);
}

// Function to set a pin as an input with a pullup
void go_pu(int pin)
{
  pinMode(pin, INPUT_PULLUP);
  digitalWrite(pin, HIGH);
}

// Function to send a pin to a logic low
void go_0(int pin)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

// Function to send a pin to a logic high
void go_1(int pin)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
}

void setup() {
  //Serial.begin(9600);
  //Serial.println("Setting up keyboard...");

  for (int a = 0; a < cols_max; a++) {  // Loop thru all column pins 
    go_pu(Col_IO[a]); // set each column pin as an input with a pullup
  }
  for (int b = 0; b < rows_max; b++) {  // Loop thru all row pins 
    go_z(Row_IO[b]); // set each row pin as a floating output
  }  
  //Optional below
  pinMode(HEARTBEAT_LED, OUTPUT); // drive the LED on the Teensy
}

boolean pad_lock = HIGH; // Initialize the pad lock to HIGH = "not pressed"
boolean Fn_pressed = HIGH; // Initialize Fn key to HIGH = "not pressed"
extern volatile uint8_t keyboard_leds; // 8 bits sent from host to Teensy that give keyboard LED status.
char blink_count = 0; // heartbeat loop counter
boolean blinky = LOW; // heartbeat LED state


void loop() {   
// Scan keyboard matrix with an outer loop that drives each row low and an inner loop that reads every column (with pull ups).
// The routine looks at each key's present state (by reading the column input pin) and also the previous state from the last scan
// that was 30msec ago. The status of a key that was just pressed or just released is sent over USB and the state is saved in the old_key matrix. 
// The keyboard keys will read as logic low if they are pressed (negative logic).
// The old_key matrix also uses negative logic (low=pressed). 

  for (int x = 0; x < rows_max; x++) {   // loop thru the rows
    go_0(Row_IO[x]); // Activate Row (send it low)
    delayMicroseconds(10); // give the row time to go low and settle out
    for (int y = 0; y < cols_max; y++) {   // loop thru the columns
      if (modifier[x][y] != 0) {  // check if modifier key exists at this location in the array (a non-zero value)
        if (!digitalRead(Col_IO[y]) && (old_key[x][y])) {  // Read column to see if key is low (pressed) and was previously not pressed
          if (modifier[x][y] != MODIFIERKEY_FN) {   // Exclude Fn modifier key  
            load_mod(modifier[x][y]); // function reads which modifier key is pressed and loads it into the appropriate mod_... variable   
            send_mod(); // function sends the state of all modifier keys over usb including the one that just got pressed
            old_key[x][y] = LOW; // Save state of key as "pressed"
          }
          else {   
            Fn_pressed = LOW; // Fn status variable is active low
            old_key[x][y] = LOW; // old_key state is "pressed" (active low)
          }
        }
        else if (digitalRead(Col_IO[y]) && (!old_key[x][y])) {  //check if key is not pressed and was previously pressed
          if (modifier[x][y] != MODIFIERKEY_FN) { // Exclude Fn modifier key 
            clear_mod(modifier[x][y]); // function reads which modifier key was released and loads 0 into the appropriate mod_... variable
            send_mod(); // function sends all mod's over usb including the one that just released
            old_key[x][y] = HIGH; // Save state of key as "not pressed"
          }
          else {
            Fn_pressed = HIGH; // Fn is no longer active
            old_key[x][y] = HIGH; // old_key state is "not pressed" 
          }
        }
      } 

      else if ((normal[x][y] != 0) || (media[x][y] != 0)) {  // check if normal or media key exists at this location in the array
        if (!digitalRead(Col_IO[y]) && (old_key[x][y]) && (!slots_full)) { // check if key pressed and not previously pressed and slots not full
          old_key[x][y] = LOW; // Save state of key as "pressed"
          if (Fn_pressed) {  // Fn_pressed is active low so it is not pressed and normal key needs to be sent
            if (keyboard_leds & 1) {  // test if Num Lock is turned on
              load_slot(numlock[x][y]); //update first available slot with key name from numlock matrix
              send_normals(); // send all slots over USB including the key that just got pressed
            }
            else if (!pad_lock) {  // test if Pad Lock is turned on (Note that Num Lock takes precedence over Pad Lock)
              load_slot(padlock[x][y]); //update first available slot with key name from padlock matrix
              send_normals(); // send all slots over USB including the key that just got pressed   
            }
            else { // Num Lock and Pad Lock are not turned on so send normal key                        
              load_slot(normal[x][y]); //update first available slot with key name from normal matrix
              //Serial.println(normal[x][y]);
              send_normals(); // send all slots over USB including the key that just got pressed
            }
          }
          else if (media[x][y] != 0) { // Fn is pressed so send media if a key exists in the matrix
            if (media[x][y] != KEY_PAD_LOCK) { // if it's not the pad lock key, send it over USB
              Keyboard.press(media[x][y]); // media key is sent using keyboard press function per PJRC    
              delay(5); // delay 5 milliseconds before releasing to make sure it gets sent over USB
              Keyboard.release(media[x][y]); // send media key release
            }
            else { // pad lock key is pushed
              pad_lock = !pad_lock; // toggle the pad_lock state
            }
          }
        }          
        else if (digitalRead(Col_IO[y]) && (!old_key[x][y])) { //check if key is not pressed, but was previously pressed 
          old_key[x][y] = HIGH; // Save state of key as "not pressed"
          if (Fn_pressed) {  // Fn is not pressed
            if (keyboard_leds & 1) {  // test if Num Lock is turned on
              clear_slot(numlock[x][y]); //clear slot with key name from numlock matrix
              send_normals(); // send all slots over USB including the key that just got released
            }
            else if (!pad_lock) {  // test if Pad Lock is turned on
              clear_slot(padlock[x][y]); //clear slot with key name from padlock matrix
              send_normals(); // send all slots over USB including the key that just got released
            }
            else {
              clear_slot(normal[x][y]); //clear slot with key name from normal matrix
              send_normals(); // send all slots over USB including the key that just got released
            }
          }
        }
      }
    }
    go_z(Row_IO[x]); // De-activate Row (send it to hi-z)
  }
  delay(24); // The overall keyboard/trackpoint scanning rate is about 30ms
}


