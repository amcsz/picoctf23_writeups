# Ready Gladiator 2

> ## Description
>
> Can you make a CoreWars warrior that wins every single round? Your opponent is the Imp. To get the flag, you must beat the Imp all 100 rounds.
>
> ## Hints
>
> - If your warrior is close, try again, it may work on subsequent tries... why is that?

## Solution

After some googling, we find out that Corewars is an old video game where programmers create programs, where the goal is to kill the other programmer's program. The battle is conducted through a space of memory. The programs are called warriors, and there are various strategies. [This](https://corewar.co.uk/strategy.htm) website contains various methods and includes a lot of corewars warriors that you can play around with.

After a bit of copy and pasting warriors from that website into the file, the Clear/Imp strategy seemed to be the most effective, so after running [this](https://corewar.co.uk/riseofthedragon.htm) warrior once, it gave a win rate of about 98. However, after a few minutes of trying this, it wasn't giving me a win of 100, so I decided to take a different approach and try to write my own redcode.

We know that all the enemy imp does is take itself and copy itself to the next position in memory, which creates an infinite loop in which the imp propagates itself through the memory. What we want to do is to stop the infinite loop. After a bit of research on [this](https://corewar-docs.readthedocs.io/en/latest/) website, I came up with this line of redcode that was able to consistently beat the imp 100% of the time:

```redcode
JMP 0, <-2
```

Let's take a look at each part of this instruction. Since redcode executes our code every clock cycle, we have used the `JMP 0` instruction to tell our program to return to itself. Basically, this does absolutely nothing except tell the program to run itself the next iteration. The `JMP` instruction does not contain a second operand, but we can still modify it.

The `<` in the `<-2` is called an addressing mode, which will basically decrement the value of the memory address after it. In this case, that memory address is two to the left, specified by `-2`(since -2 is two left of the current position on the number line). It really doesn't matter what the number is, as long as it is to the negative, or to the left, of your position in memory(as the imp is moving right).

Since the imp's code is `MOV 0, 1`, it will decrement it's instruction to `MOV 0, 0`. This will cause the imp to stop moving. However, since the imp's pointer is still pointing at the next address, it will then die. This is because, according to the corewars documentation,

> By default all instructions within the Core are initialised to: DAT.F $0, $0 which are Dat instructions.

Since `DAT` instructions cause all warriors to terminate, and the imp is pointing at one, the imp is die on its own. This is what the memory looks like right before the imp dies:

```redcode
Address: MOV 0, 1 ; imp before it dies
Address: MOV 0, 0 ; instruction where it gets decremented
Address: DAT.F $0, $0 ; deadly dat instruction that kills imp
Address: JMP 0, <-2 ; our code
```

This works 100% of the time because no matter what, the imp will always find itself a position where it will get decremented, since it keeps on moving itself through every position in memory. Our flag:

```shell
Rounds: 100
Warrior 1 wins: 100
Warrior 2 wins: 0
Ties: 0
You did it!
picoCTF{redacted}
```
