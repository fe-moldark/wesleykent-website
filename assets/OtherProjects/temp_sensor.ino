//LiquidCrystal Library for the LCD
#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//Temp sensor
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

//Define LCD screen
const int rs = 7, en = 8, d4 = 9, d5 = 10, d6 = 11, d7 = 12;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


void setup() {
  Serial.begin(9600);
  sensors.begin();

  //First lines
  lcd.begin(16, 2);
  lcd.print("    WELCOME    ");
  lcd.setCursor(0, 1);
  lcd.print("     <NAME>      ");
}

void loop() {
  //Update every two seconds
  delay(2000);
  lcd.clear();

  //Line One
  lcd.setCursor(0, 0);
  lcd.print("Temperature:");

  //Request temperatures
  lcd.setCursor(0, 1);
  sensors.requestTemperatures();
  lcd.print(sensors.getTempFByIndex(0));
}

