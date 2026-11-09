# 2026 United States Grand Prix: Top 5 Analysis

Hello!

Welcome to the first installment in my personal analysis of Formula 1 data!

In this installment, we will be looking at the 2026 United States Grand Prix at the Circuit of The Americas (COTA). Specifically, I have drawn data from the top five finishers during their race. We will be looking at lap times, tyre compounds, average speeds, and strategy. All work is done utilizing python and the FASTF1 API.

## Context

At this year’s USA GP, we saw Kimi Antonelli, on the break of clinching his first world championship, start on pole position. He was followed by the RedBulls, Max Verstappen (VER) and Isack Hadjar respectively, with the two Ferraris, Charles Leclerc (LEC) and Lewis Hamilton (HAM) rounding off the top five.

## Tyre of Choice

The hard tyre was the way to go this year at COTA. LEC clocked the fastest lap with a 1:37.976 on lap 42 using this hard tyre. Looking at our “Lap Time Distribution on Tyre Compound” visual, we can see this tyre choice reflected. Four of our top five ran the hard tyre during the race, and it consistently put in fastest laps they had. This visual also gives us insight to the pace of the teams throughout the race. Ferrari was the quickest car, however, they were inconsistent. The other teams running hards, Mercedes and McLaren, also used the hard tyre on their fastest laps, but were much more consistent. The most baffling piece of this visual, is VER. We can see that he did not use the hard tyre at all throughout the race and was still able to score a podium!

## What happened to Ferrari?

As we mentioned before, Ferrari clearly was the fastest team on the tyre of choice this weekend. But when we look at the overall strategy, we can see why this may have stopped them from securing a win. They both started on the soft tyre (grippiest, but susceptible to degradation). While the soft did give them a great start and the ability to fight for positions early, it lasted for only about 15-20 laps. This caused the two (along with others) to pit early. The prancing horses were able to claw their way back up to fight for the podium positions. At the end of the race, VER mediums started to fail him and he was caught by LEC on his lighting-fast hards for P2. HAM was looking like he was in great position to secure P3. Looking at “Lap Times Across Race: Top 5 Finishers”, we can see just how much faster HAM was than VER. However, a safety car on lap 51 ended the pursuit.

## Strategy Analysis

For this section, all details will be referring to the “Strategies” visual. Strategists were calling for a two stop this weekend. The soft look is quick and relatively durable, shifting focus away from the longer-lasting hard tyre. However, we saw quite the opposite.

Our winner, ANT, went for the one-stop and it paid off. Everyone else in the top five started on softs, besides NOR who started on mediums as well. What was the key for ANT strategy? His lap times were as fast as those on softs around him (“Lap Time Distribution on Tyre Compound”), but he was able to keep that tyre on for much longer, building a gap and fresh air for a pit stop to hards. Now on the fastest hard tyre, he was able to quickly catch up and overtake LEC for P1.

The Ferraris (disappointment in their strategy analysis may be consistent through these installments) went for the expected strategy. The two-stop still worked very well. What would have secured them a 2-3 was ruined by the safety car at the most critical moment.

The two outliers we have are obviously NOR and VER. I think it is easier to start with NOR. We can see he used the same one-stop strategy as ANT, but boxed much earlier than ANT. He got on the faster tyre much earlier, which did allow him to increase his pace. However, when the tyres got old, he started to tumble down the order. NOR was also at a lack of pace in general this weekend, visible in the other graphs.

VER, like the Ferraris that sandwiched him, started on the softs. They chose an alternative strategy, attempting an undercut onto another set of soft tyres. This initially looked like the wrong choice. Teams are required to use two different tyre compounds throughout a race, so going back on to the short-lasting soft seemed like a death sentence. However, VER was able to make them last. He got on to a set of mediums with a manageable amount of laps left, but with two red-hot Ferraris on his tail. One managed to get him LEC, as mentioned earlier. It was looking like it was over as HAM approached rapidly. VER was luckily saved by the bell with a late safety car neutralizing the race.

## Takeaways

ANT showed us how cool heads can prevail. Everyone around him was frantically looking for as much pace as possible; electing to use the faster tyre seemed like the best way to seal this race. However, the Mercedes team took a step back, and with the championship in mind, chose to play it safe. The two stops were different but effective when playing the long game. NOR would have fallen in the same boat as ANT had their car intrinsically had more pace. An aspect I am sure they are already aware of. As for Ferrari and RBR, strategy changes must be made. Avid Formula 1 fans are aware of Ferrari’s “brilliant” strategic choices, but this was a surprise from RBR. Normally, they are able to keep the whole race in mind, but clearly messed up this weekend. They were saved really by luck with a safety car, and VER really showing everyone why he is a four-time world champion.
