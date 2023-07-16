#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from operator import index, indexOf
import spade
from spade.agent import Agent
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, PeriodicBehaviour
import random
from spade import quit_spade
import time

from deck import Deck

globalneKarteIgracA=[]
globalneKarteIgracB=[]
globalnaZadnjaKarta=[]


class Okruzje(Agent):
  class PosaljiPoruku(PeriodicBehaviour):
    async def on_start(self):
      self.counter=0
      self.deck = Deck()
      self.spilKarata = self.deck.cards
      self.igracAKarte=[]
      self.igracBKarte=[]
      self.igracAPoeni=[]
      self.igracBPoeni=[]
      self.prednost=True
      self.baceneKarte=[]
      self.igracAbodovi=0
      self.igracBbodovi=0

      

    async def run(self):
      self.counter += 1
      if self.counter==1:
        print("----------------Napravio sam spil talijanskih karata-------")
        #dodaj prve 4 karte igracu A
        self.igracAKarte.append(self.spilKarata.pop())
        self.igracAKarte.append(self.spilKarata.pop())
        self.igracAKarte.append(self.spilKarata.pop())
        self.igracAKarte.append(self.spilKarata.pop())

        print("Dodavanje globalnoj listi karte igraca A")
        for a in self.igracAKarte:
          globalneKarteIgracA.append(a)
          a.get_visual()
        #dodaj prve 3 karte igracu B
        self.igracBKarte.append(self.spilKarata.pop())
        self.igracBKarte.append(self.spilKarata.pop())
        self.igracBKarte.append(self.spilKarata.pop())
        self.igracBKarte.append(self.spilKarata.pop())

        print("Dodavanje globalnoj listi karte igraca B")
        for b in self.igracBKarte:
          globalneKarteIgracB.append(b)
          b.get_visual()
        
        print(len(self.spilKarata.cards))
        globalnaZadnjaKarta.append(self.spilKarata.cards[0])
        msg = spade.message.Message(
          to="vrba1@localhost",
          body="prviPotez")

        await self.send(msg)
        
        msg = spade.message.Message(
          to="vrbaa2@localhost",
          body="prviPotez")

        await self.send(msg)

      else:
        msg = await self.receive(timeout=100)      
        if msg:
          #self.sadrzaj.append(msg.body)
          if msg.sender.domain=="vrba1":
            if msg.metadata:
              print("igrac A je prvi na potezu")
              print(f"Okruzije: IgracA je odlucio baciti")
              if len(self.igracAKarte)!=0:
                self.baceneKarte.append(self.igracAKarte[int(msg.body)])
                self.igracAKarte[int(msg.body)].ispis()
                self.igracAKarte.pop(int(msg.body))
                globalneKarteIgracA.pop(int(msg.body))
                self.prednost=True

            else:
              print("igrac B je prvi na potezu")
              print("Okruzije: IgracA je odlucio baciti")
              if len(self.igracAKarte)!=0:
                self.baceneKarte.append(self.igracAKarte[int(msg.body)])
                self.igracAKarte[int(msg.body)].ispis()
                self.igracAKarte.pop(int(msg.body))
                globalneKarteIgracA.pop(int(msg.body))
                self.prednost=False

          
          if msg.sender.domain=="vrbaa2":
            print("Okruzije: IgracB je odlucio baciti:")
            if len(self.igracBKarte)!=0:
              self.baceneKarte.append(self.igracBKarte[int(msg.body)])
              self.igracBKarte[int(msg.body)].ispis()
              self.igracBKarte.pop(int(msg.body))
              globalneKarteIgracB.pop(int(msg.body))
            
          
          if len(self.baceneKarte)==2:
            if self.prednost==True:
              #print("napravi odluku kada igrac A baca prvi")
              if(self.baceneKarte[0].boja == globalnaZadnjaKarta[0].boja):
                if(self.baceneKarte[1].boja != globalnaZadnjaKarta[0].boja):
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  print("Igrac A osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                    for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                    for bodB in self.igracBPoeni:
                      self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                      bodB.ispis()
                    print("Agent A")
                    print(self.igracAbodovi)
                    print("Agent B")
                    print(self.igracBbodovi)

                  if len(self.spilKarata.spil)!=0:
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)

                else:#oba igraca su odigrali briskulu odnosno adut
                  if(self.baceneKarte[0].vrijednost>self.baceneKarte[1].vrijednost):
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    print("Igrac A osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)

                  elif(self.baceneKarte[0].vrijednost==self.baceneKarte[1].vrijednost):
                    if(self.baceneKarte[0].brojka>self.baceneKarte[1].brojka):
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      print("Igrac A osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                          bodA.ispis()
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                          bodB.ispis()
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)
                    else:
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      print("Igrac B osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                          bodA.ispis()
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                          bodB.ispis()
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)
                  else:
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    print("Igrac B osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)
              else:
                if(self.baceneKarte[1].boja == globalnaZadnjaKarta[0].boja):
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  print("Igrac B osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                  if len(self.spilKarata.spil)!=0:
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)

                elif(self.baceneKarte[0].boja == self.baceneKarte[1].boja): #boje jednake

                  if(self.baceneKarte[0].vrijednost>self.baceneKarte[1].vrijednost):
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    print("Igrac A osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)
                  

                  elif(self.baceneKarte[0].vrijednost==self.baceneKarte[1].vrijednost):
                    if(self.baceneKarte[0].brojka>self.baceneKarte[1].brojka):
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      print("Igrac A osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)

                    else:
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      print("Igrac B osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)
                  else:
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    print("Igrac B osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)
                  
                else:#znaci da ni A ni B nisu igrali aduta a B nije postivao boju
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  print("Igrac A osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                  if len(self.spilKarata.spil)!=0:
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)

                

            else:
              print("napravi odluku kada igrac B baca prvi")
              #self.baceneKarte.reverse()
              if(self.baceneKarte[0].boja == globalnaZadnjaKarta[0].boja):
                if(self.baceneKarte[1].boja != globalnaZadnjaKarta[0].boja):
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  print("Igrac B osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                  if len(self.spilKarata.spil)!=0:
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)

                else:#oba igraca su odigrali briskulu odnosno adut
                  if(self.baceneKarte[0].vrijednost>self.baceneKarte[1].vrijednost):
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    print("Igrac B osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)

                  elif(self.baceneKarte[0].vrijednost==self.baceneKarte[1].vrijednost):
                    if(self.baceneKarte[0].brojka>self.baceneKarte[1].brojka):
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      print("Igrac B osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)

                    else:
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      print("Igrac A osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)

                  else:
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    print("Igrac A osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)

              else:
                if(self.baceneKarte[1].boja == globalnaZadnjaKarta[0].boja):
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  self.igracAPoeni.append(self.baceneKarte.pop())
                  print("Igrac A osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                  if len(self.spilKarata.spil)!=0:
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)

                elif(self.baceneKarte[0].boja == self.baceneKarte[1].boja): #boje jednake

                  if(self.baceneKarte[0].vrijednost>self.baceneKarte[1].vrijednost):
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    self.igracBPoeni.append(self.baceneKarte.pop())
                    print("Igrac B osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                    if len(self.spilKarata.spil)!=0:
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)


                  elif(self.baceneKarte[0].vrijednost==self.baceneKarte[1].vrijednost):
                    if(self.baceneKarte[0].brojka>self.baceneKarte[1].brojka):
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      self.igracBPoeni.append(self.baceneKarte.pop())
                      print("Igrac B osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                      if len(self.spilKarata.spil)!=0:
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)

                    else:
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      self.igracAPoeni.append(self.baceneKarte.pop())
                      print("Igrac A osvojio poen")
                      if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                        for bodA in self.igracAPoeni:
                          self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        for bodB in self.igracBPoeni:
                          self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        print("Agent A")
                        print(self.igracAbodovi)
                        print("Agent B")
                        print(self.igracBbodovi)
                        self.kill(exit_code=10)
                        return
                        
                      if len(self.spilKarata.spil)!=0:
                        self.igracAKarte.append(self.spilKarata.spil.pop())
                        self.igracBKarte.append(self.spilKarata.spil.pop())
                        globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                        globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                      msg = spade.message.Message(
                      to="vrba1@yax.im",
                      body="imamPrednost")
                      await self.send(msg)
                      
                      msg = spade.message.Message(
                      to="vrbaa2@yax.im",
                      body="nemamPrednost")
                      await self.send(msg)

                  else:
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    self.igracAPoeni.append(self.baceneKarte.pop())
                    print("Igrac A osvojio poen")
                    if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                        bodA.ispis()
                      for bodB in self.igracBPoeni:
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                        bodB.ispis()
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                      
                    if len(self.spilKarata.spil)!=0:
                      self.igracAKarte.append(self.spilKarata.spil.pop())
                      self.igracBKarte.append(self.spilKarata.spil.pop())
                      globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                      globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                    msg = spade.message.Message(
                    to="vrba1@yax.im",
                    body="imamPrednost")
                    await self.send(msg)
                    
                    msg = spade.message.Message(
                    to="vrbaa2@yax.im",
                    body="nemamPrednost")
                    await self.send(msg)

                  
                else:#znaci da ni A ni B nisu igrali aduta a A nije postivao boju
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  self.igracBPoeni.append(self.baceneKarte.pop())
                  print("Igrac B osvojio poen")
                  if(len(self.igracAPoeni)+len(self.igracBPoeni)==40):
                      for bodA in self.igracAPoeni:
                        bodA.ispis()
                        self.igracAbodovi=self.igracAbodovi+int(bodA.vrijednost)
                      for bodB in self.igracBPoeni:
                        bodB.ispis()
                        self.igracBbodovi=self.igracBbodovi+int(bodB.vrijednost)
                      print("Agent A")
                      print(self.igracAbodovi)
                      print("Agent B")
                      print(self.igracBbodovi)
                      self.kill(exit_code=10)
                      return
                  if len(self.spilKarata.spil)!=0:
                    self.igracBKarte.append(self.spilKarata.spil.pop())
                    self.igracAKarte.append(self.spilKarata.spil.pop())
                    globalneKarteIgracA.append(self.igracAKarte[len(self.igracAKarte)-1])
                    globalneKarteIgracB.append(self.igracBKarte[len(self.igracBKarte)-1])

                  msg = spade.message.Message(
                  to="vrbaa2@yax.im",
                  body="imamPrednost")
                  await self.send(msg)
                  
                  msg = spade.message.Message(
                  to="vrba1@yax.im",
                  body="nemamPrednost")
                  await self.send(msg)


  async def setup(self):
    print("Okruzije: Pokrećem se!")
    start_at = datetime.datetime.now() + datetime.timedelta(seconds=6)
    ponasanje = self.PosaljiPoruku(period=1, start_at=start_at)
    self.add_behaviour(ponasanje)   

class IgracA(Agent):
  class SvePoruke(CyclicBehaviour):
    async def on_start(self):
      self.sadrzaj = []
      self.brojacA=0
    
    async def run(self):
      msg = await self.receive(timeout=100)

      if msg:
        #print(self.brojacA)
        self.brojacA=self.brojacA+1
        #self.sadrzaj.append(msg.body)
        print(f"AgentA: Dobio sam: {msg.body} \n")
        if msg.body=="prviPotez":
          for a in globalneKarteIgracA:
            self.sadrzaj.append(a)
          print("dodao sam sadrzaj globalnih karata u sadrzaj svojih karata")
          odabranaKarata=0

          msg = spade.message.Message(
          to="vrbaa3@localhost",
          body=str(odabranaKarata),
          sender="vrba1",
          metadata={"bacio": "0 kartu"})
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKarata)

        elif msg.body=="imamPrednost":
          if self.brojacA<17:
            self.sadrzaj.append(globalneKarteIgracA[len(globalneKarteIgracA)-1])
          #print("AgentA:napravi algoritam sa prednošću")
          odabranaKarata=random.randint(0,len(self.sadrzaj)-1)
          msg = spade.message.Message(
          to="vrbaa3@localhost",
          body=str(odabranaKarata),
          sender="vrba1",
          metadata={"bacio": "0 kartu"})
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKarata)

        elif msg.body=="nemamPrednost":
          if self.brojacA<17:
            self.sadrzaj.append(globalneKarteIgracA[len(globalneKarteIgracA)-1])
          #print("AgentA:napravi algoritam kad si 2 na redu")
          minimalnaKarta=10
          indexMinimalneKarte=0
          for a in self.sadrzaj:
            if a.vrijednost<minimalnaKarta:
              minimalnaKarta=a.vrijednost
              indexMinimalneKarte=indexOf(self.sadrzaj,a)

          odabranaKarata=indexMinimalneKarte
          msg = spade.message.Message(
          to="vrbaa3@localhost",
          body=str(odabranaKarata),
          sender="vrba1")
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKarata)
          

       # for k in self.sadrzaj:
       #   k.ispis()
       # print("")
        if self.brojacA<18:
          self.sadrzaj.pop(odabranaKarata)
        
      else:
        print("IgracA: Čekao sam, ali nema poruke.")

              
  async def setup(self):
      print("IgracA: Pokrećem se!")
      ponasanjeSve = self.SvePoruke()
      self.add_behaviour(ponasanjeSve)

class IgracB(Agent):
  class SvePoruke2(CyclicBehaviour):
    async def on_start(self):
      self.sadrzaj = []
      self.brojacB=0
    
    async def run(self):
      msg = await self.receive(timeout=100)
      if msg:
        #print(self.brojacB)
        self.brojacB=1+self.brojacB
        if msg.body=="prviPotez":
          for b in globalneKarteIgracB:
            self.sadrzaj.append(b)
          print("AgentB:Dodao sam sadrzaj globalnih karata u svoj sadrzaj")
          odabranaKartaB=1

          msg = spade.message.Message(
          to="vrbaa3@jabber.fr",
          body=str(odabranaKartaB),
          sender="vrbaa2",
          metadata={"bacio": "0 kartu"})
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKartaB)
        
        elif msg.body=="imamPrednost":
          if self.brojacB<17:
            self.sadrzaj.append(globalneKarteIgracB[len(globalneKarteIgracB)-1])
          #print("AgentB:napravi algoritam sa prednošću")
          odabranaKartaB=random.randint(0,len(self.sadrzaj)-1)
          msg = spade.message.Message(
          to="vrbaa3@jabber.fr",
          body=str(odabranaKartaB),
          sender="vrbaa2")
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKartaB)

        elif msg.body=="nemamPrednost":
          if self.brojacB<17:
            self.sadrzaj.append(globalneKarteIgracB[len(globalneKarteIgracB)-1])
          #print("AgentB:napravi algoritam kad si 2 na redu")
          maksimalnaKarta=0
          indexMaksimalneKarte=0
          for a in self.sadrzaj:
            if a.vrijednost>maksimalnaKarta:
              maksimalnaKarta=a.vrijednost
              indexMaksimalneKarte=indexOf(self.sadrzaj,a)

          odabranaKartaB=indexMaksimalneKarte
          #print("max karta")
          #print(odabranaKartaB)
          msg = spade.message.Message(
          to="vrbaa3@jabber.fr",
          body=str(odabranaKartaB),
          sender="vrbaa2")
          await self.send(msg)
          #self.sadrzaj.pop(odabranaKartaB)

      #  for k in self.sadrzaj:
      #    k.ispis()
      #  print("")
        if self.brojacB<18:
          self.sadrzaj.pop(odabranaKartaB)

      else:
        print("IgracB: Čekao sam, ali nema poruke.")
              
  async def setup(self):
      print("IgracB: Pokrećem se!")
      ponasanjeSve2 = self.SvePoruke2()
      self.add_behaviour(ponasanjeSve2)



if __name__ == '__main__':
    igracA = IgracA("vrba1@yax.im", "tajna")
    igracA.start()

    time.sleep(1.5)

    igracB = IgracB("vrbaa2@yax.im", "tajna")
    igracB.start()

    time.sleep(1.5)
    okruzije = Okruzje("vrbaa3@jabber.fr", "tajna")
    okruzije.start()

    time.sleep(1.5)
    input("Press ENTER to exit.\n")
    igracA.stop()
    igracB.stop()
    okruzije.stop()
    quit_spade()

