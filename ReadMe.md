# LOCM_Agent
![](./assets/teaser.png)
<center>
Provided by DALL-E
</center>

## What's Here
1. This repo contained agents based on heuristic algorithm for [LOCM](https://www.codingame.com/ide/puzzle/legends-of-code-magic)
2. Code reproduction of the [CCG competitions](https://github.com/acatai/Strategy-Card-Game-AI-Competition/tree/master) over the years on the existing benchmarks.
3. Based on existing benchmarks, methods including minmax, Monte Carlo and beam search are provided here


## leaderboard

Here is the corresponding ranking and other relevant information when submitting the code.  
This ranking may ***change dynamically***, depending on the agent's ability, number of agents in the current level, submission time and etc..

| Methods | League Level & Rank | Win Rate | Level Score |
| -------- | :--------: | :----: | :----: |
| Easy-Ruled   | Bronze 654/1360    | 57%  |18.72|
| UJIAGENT1   | Bronze  299/1360 | 65%  |21.56|
| MugenSlayerAttackOnDuraraBallV3| Silver 332/394 | 51%  |15.67|
| UJIAGENT2   | Silver  297/394 | 52%  |16.29|
| MinMaxAgent | Silver  130/384 | 54%  |17.18|
| MonteCorleAgent| Silver  126/384 | 56%  |17.98|
| BeamSearchAgent| Silver  122/384 | 58% |18.42|
<!-- |    | Silver   | 65%  | -->

## TimeLine/MileStones

- [x] 2024-06-07: Finish An Agent Based on Human Experiences of Playing HeartStone.
- [x] 2024-07-05: Implement Some Baseline From CCG 2020/2021 and Modified to Adapt Rules for Now. 
- [x] 2024-07-21: MinMax agent is finished, use this agent we achieve silver first time.
- [x] 2024-07-25: BeamSearch Agent is finished, provides a wider range of search strategies
- [x] 2024-08-16: MontoCarlo Agent is finished, based on the code of BeamSearch Agent