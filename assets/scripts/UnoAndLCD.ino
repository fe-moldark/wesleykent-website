#define LCD_CS 33 // Chip Select goes to Analog 3
#define LCD_CD 15 // Command/Data goes to Analog 2
#define LCD_WR 4 // LCD Write goes to Analog 1
#define LCD_RD 2 // LCD Read goes to Analog 0
#define LCD_RESET 32 // Can alternately just connect to Arduino's reset pin

#include <SD.h>
#define sd_cs  10

#include <SPI.h>          // f.k. for Arduino-1.5.2
#include "Adafruit_GFX.h"// Hardware-specific library
#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;

#define	BLACK   0x0000
#define WHITE   0xFFFF

#ifndef min
#define min(a, b) (((a) < (b)) ? (a) : (b))
#endif

void setup(void);
void loop(void);
unsigned long FillScreen();


uint16_t g_identifier;

extern const uint8_t hanzi[];


void setup(void) {
    Serial.begin(9600);
    uint32_t when = millis();

    if (!Serial) delay(5000);
    Serial.println("Serial took " + String((millis() - when)) + "ms to start");

    uint16_t ID = tft.readID();
    Serial.print("ID = 0x");
    Serial.println(ID, HEX);
    if (ID == 0xD3D3) ID = 0x9481;
    tft.begin(ID);

    if (!SD.begin(sd_cs)) {
      Serial.println("Well it failed but fuck it just keep going.");
    }

    Serial.println("Initialization done.");
}

void printmsg(int row, const char *msg)
{
    tft.setTextColor(WHITE, BLACK);
    tft.setCursor(0, row);
    tft.println(msg);
}

void loop(void) {
    uint8_t aspect;
    uint16_t pixel;
    const char *aspectname[] = {
        "PORTRAIT", "LANDSCAPE", "PORTRAIT_REV", "LANDSCAPE_REV"
    };
    const char *colorname[] = { "BLUE", "GREEN", "RED", "GRAY" };
    uint16_t colormask[] = { 0x001F, 0x07E0, 0xF800, 0xFFFF };
    uint16_t dx, rgb, n, wid, ht, msglin;
    tft.setRotation(180);
    FillScreen();
    delay(100);
    
    tft.invertDisplay(false);
    delay(100);
    tft.invertDisplay(false);
}

typedef struct {
    PGM_P msg;
    uint32_t ms;
} TEST;
TEST result[12];

unsigned long FillScreen() {

    File root = SD.open("/");
    if (!root) {
      Serial.println("Failed to open sd card / its directory");
      return;
    } else {
      Serial.print("NO ERRORS");
    }

    while (true) {
      File entry = root.openNextFile();
      if (!entry) {
        break;
      }

      if (strstr(entry.name(), ".BMP") != NULL) {
        drawBMP(entry.name());
      }
      entry.close();
    }
    root.close();
    delay(2000);
}


void drawBMP(const char *filename) {
  File bmpFile = SD.open(filename);

  if (!bmpFile) {
    Serial.println("Error opening the BMP file");
    return;
  }

  uint32_t fileSize = bmpFile.size();
  uint16_t imgOffset = 135; //Needed to adjust this for whatever reason from 0
  bmpFile.seek(18);
  uint32_t imgWidth = bmpFile.read() | (bmpFile.read() << 8) | (bmpFile.read() << 16) | (bmpFile.read() << 24);
  uint32_t imgHeight = bmpFile.read() | (bmpFile.read() << 8) | (bmpFile.read() << 16) | (bmpFile.read() << 24);

  // Adjust starting coordinates
  int startX = (tft.width() - imgWidth) / 2 ;  // Center the image horizontally
  int startY = (tft.height() - imgHeight) / 2;  // Center the image vertically

  // Draw BMP image pixel by pixel
  for (int y = 0; y < imgHeight; y++) {
    for (int x = 0; x < imgWidth; x++) {
      bmpFile.seek(imgOffset + (x + (imgHeight - 1 - y) * imgWidth) * 3);  // 3 bytes per pixel (BGR)
      uint8_t blue = bmpFile.read();
      uint8_t green = bmpFile.read();
      uint8_t red = bmpFile.read();
      
      uint16_t color = tft.color565(red, green, blue);
      tft.drawPixel(startX + x, startY + y, color);
    }
  }

  bmpFile.close();
}
