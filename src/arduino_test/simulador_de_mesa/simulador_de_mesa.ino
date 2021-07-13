#include <modbus.h>
#include <modbusDevice.h>
#include <modbusRegBank.h>
#include <modbusSlave.h>

modbusDevice regBank;

modbusSlave slave;

void setup() {
  regBank.setId(1);

  regBank.add(40513); //definir posX  
  regBank.add(40529); //definir posY 
  regBank.add(40545); //definir velocidade do eixo X  
  regBank.add(40561); //definir velocidade do eixo Y 
  regBank.add(40221); //visualizar posX 
  regBank.add(40231); //visualizar posY

  
  slave._device = &regBank;  
 
  slave.setBaud(9600);

  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
}

void loop() {
 
  regBank.set(40221,0);
  regBank.set(40231,0);
  regBank.set(40513,0);
  regBank.set(40529,0);
  regBank.set(40545,0);
  regBank.set(40561,0);

  while(1)
  {
    
   int def_x = regBank.get(40513);
   int def_y = regBank.get(40529);
   int act_x = regBank.get(40221);
   int act_y = regBank.get(40231);
   
   //Movimentar no eixo X
   if(def_x>act_x)
   {
     for (act_x; act_x<=def_x; act_x++)
     {
      regBank.set(40221, act_x);
      digitalWrite(2,HIGH);
     }
   }
   if(def_x<act_x)
   {
    for (act_x; act_x>=def_x; act_x--)
     {
      regBank.set(40221, act_x);
      digitalWrite(2,HIGH);
     }
   }

   //Movimentar no eixo Y
   if(def_y>act_y)
   {
     for(act_y; act_y<=def_y; act_y++)
     {
      regBank.set(40231, act_y);
      digitalWrite(3,HIGH);
     }
   }
   if(def_y<act_y)
   {
    for (act_y; act_y>=def_y; act_y--)
     {
      regBank.set(40231, act_y);
      digitalWrite(3,HIGH);
     }
   }

   digitalWrite(2,LOW);
   digitalWrite(3,LOW);
   slave.run(); 
  }

}
