float X;     // variable to X data
float Y;     // variable to Y data

void setup() // runs once when the sketch starts
{  
  Serial.begin(9600); // initialize serial communication
}


double randomDouble(double minf, double maxf)
{
  return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31);  // use 1ULL<<63 for max double values)
}

void loop() // runs repeatedly after setup() finishes
{
  X =  randomDouble((0.1, 60.0),61.3);         // read X vernier
  Y = randomDouble((0.1, 58.0),59.5);         // read X vernier
  Serial.println(X);         // send data to serial
  Serial.println(Y);         // send data to serial
   delay(100);             // Pause 100 milliseconds
}
