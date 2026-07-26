# Week 4 Practice Talk Script
**"Method in plain English" · ~3 minutes**

---

## Slide 1 — Title (~20 sec)

- I'm Oussama. I'm building a model to predict which U.S. banks are heading toward trouble, before it happens.
- This week the job wasn't building a model. A computer can hand you one in seconds. The job was choosing the right kind, and being able to say why.
- So that's what I'll walk you through: the choice I made, and whether it actually earns its place.

---

## Slide 2 — Two ways to score a bank (~70 sec)

- There are two ways to score how risky a bank is.
- The simple way: take each warning sign on its own, capital, bad loans, profit, and add them up into one score. It's easy to explain, and that matters, because regulators want to know why a bank got flagged.
- But it has a blind spot. It can't tell that falling capital is far more dangerous when bad loans are climbing at the same time. It treats each sign as if the others aren't there.
- The way I chose instead: let the model learn the combinations of warning signs that showed up before real trouble. Not each sign alone, but how they move together.
- That's harder to explain, so I add a tool that shows which signs drove each warning. That's the trade I'm making: a little transparency, for the ability to see the whole picture.
- And here's why that trade is worth it for my project. My main finding was that six warning signs slide down together for two years before a bank fails. Only the second approach can even see the word "together."

---

## Slide 3 — Does it earn its keep? (~70 sec)

- So does the more complex model actually earn its place? I tested it honestly, and the answer is: it depends.
- On the left, a crisis like the ones it learned from. Here the model clearly beats the simple rule, by a wide margin. It works.
- On the right, a new kind of crisis it had never seen, the 2023 bank runs. Here it loses. The simple rule does better.
- That's not a broken model. It's a model taught the wrong lesson. It learned from decades of banks that failed slowly, from bad loans. But the 2023 failures were fast, driven by depositors pulling money out overnight, something the old failures never showed it.
- And that points straight at my next step. The warning for those new failures was in the data, just not where the model was looking. It was in the deposits leaving, not the capital. So next I build features that track those trends over time.
- The honest takeaway: the method is the right choice, but only once I feed it the signals that match today's failures. That's what I'm doing next.

---

## Notes to self before recording

- The talk carries the "why," the slides just anchor it. Don't read the slides.
- Slow down on the two blind spots: "together" on slide 2, and "taught the wrong lesson" on slide 3.
- Don't hide the loss on slide 3. Owning it is the strongest part.
- Land the last line and stop.
