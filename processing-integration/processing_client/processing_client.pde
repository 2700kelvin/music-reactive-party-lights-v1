import processing.net.*; 

/*
Warning: This file is quite old and I haven't tested it in some time.
*/

Client myClient; 

int numPixels = 150;
int bufferSize = 3 * numPixels;

byte[] byteBuffer = new byte[bufferSize];
byte interesting = 127;

int convert(byte x) {
  return x & 0xff;
}

void setup() { 
  size(1200, 200);
  myClient = new Client(this, "127.0.0.1", 12345);
  frameRate(200);
} 

void draw() { 
  if (myClient.available() >bufferSize) { 
  // if (myClient.available() > 0) { 
    int byteCount = myClient.readBytes(byteBuffer); 
    if(byteCount != bufferSize) {
      print("Bytes received not same as buffer size");
      exit();
    }
    //for (int i = 0; i < byteCount; i++) {
    //  print(convert(byteBuffer[i]));
    //  print(',');
    //}
    //println();
    drawBuffer();
  }
}
/*
 rect(a, b, c, d)
 rect(a, b, c, d, r)
 rect(a, b, c, d, tl, tr, br, bl)
 
 Parameters  
 a   float: x-coordinate of the rectangle by default
 b   float: y-coordinate of the rectangle by default
 c   float: width of the rectangle by default
 d   float: height of the rectangle by default
 */
void drawBuffer() {
  int pWidth = width / numPixels;
  for (int pixelNum = 0; pixelNum < numPixels; pixelNum++) {
    int r = convert(byteBuffer[pixelNum * 3]);
    int g = convert(byteBuffer[pixelNum * 3 + 1]);
    int b = convert(byteBuffer[pixelNum * 3 + 2]);
    fill(r, g, b);
    int x = pWidth * pixelNum;
    rect(x, 0, pWidth, height);
  }
}