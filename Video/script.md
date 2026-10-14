# Script: Strassen's Algorithm - Beating n³

length is 7 min (about 1050 words at 150 wpm)
Visual split: PowerPoint 60% (4:12), IDE 30% (2:06), Manim 10% (0:42).

Visual keys: **[SLIDES n]** = `Strassen.pptx` slide n · **[IDE]** = `Strassen\Program.cs` · **[MANIM]** = `strassen_cancellation.py`

| #   | Time      | Visual      | Share |
| --- | --------- | ----------- | ----- |
| 1   | 0:00-0:35 | SLIDES 1-2  |       |
| 2   | 0:35-1:35 | SLIDES 3-4  |       |
| 3   | 1:35-2:17 | MANIM       | 10%   |
| 4   | 2:17-4:23 | IDE         | 30%   |
| 5   | 4:23-5:38 | SLIDES 5-6  |       |
| 6   | 5:38-6:18 | SLIDES 7    |       |
| 7   | 6:18-7:00 | SLIDES 8-10 |       |

---

## Segment 1 - The problem (0:00-0:35) · **[SLIDES 1-2]**

_Slide 1: portrait of Volker Strassen + title. Slide 2: the n³ table._

> Multiplying two matrices is one of the most important things a computer does. It sort of sits underneath neural networks, graphics and ray tracing, and some linear equation solvers so if you marked my assignment 1 you might know what i mean.
>
> The textbook method takes each of the n-squared entries of the answer and computes a sum of n products. That's n-cubed multiplications. Double the matrix size, and the work goes up eight times.
>
> For centuries, everyone assumed you could not do better. Then in 1969, Volker Strassen published a three-page paper with a title that started with the words: "Gaussian elimination is not optimal". He proved n-cubed was beatable. This is how.

(~95 words)

---

## Segment 2 - How it works (0:35-1:35) · **[SLIDES 3-4]**

_Slide 3: coloured 2×2 block diagram. Slide 4: Strassen diagram (Wikimedia) + the seven formulas._

> Start with divide and conquer. Cut each matrix into four quadrants, each half the size. Multiplying them out block by block, the answer's top-left quadrant is A11 times B11, plus A12 times B21, and so on. That is eight half-size multiplications, and eight recursive calls gives you exactly n-cubed again. No progress.
>
> Strassen's insight: a multiplication of big blocks is expensive, but adding blocks is cheap. So he found seven clever products, M1 to M7, each built from sums and differences of the quadrants. For example, M1 is A11 plus A22, times B11 plus B22.
>
> Then the four answer quadrants are rebuilt using only additions and subtractions of those seven. C11 is M1 plus M4 minus M5 plus M7. We have traded one multiplication for a handful of additions. But why does that give the right answer? Let's watch the algebra cancel.

(~150 words)

---

## Segment 3 - Why the combination works (1:35-2:17) · **[MANIM]**

_Animation: expand M1, M4, −M5, M7 into twelve raw terms; five pairs light up and cross out; only A11B11 and A12B21 survive._

> Expand the four products that make C11. That's twelve raw terms. Look at A11B22: M1 contributes a positive copy, and M5 contributes a negative one. They cancel. A22B11: positive in M1, negative in M4. Gone. A22B22: positive in M1, negative in M7. A22B21: positive in M4, negative in M7. And A12B22, negative in M5, positive in M7.
>
> Five pairs cancel, ten terms vanish, and what's left is A11B11 plus A12B21. That's exactly the classical answer for C11, but we got there with seven multiplications overall instead of eight. The other three quadrants cancel in the same way.

(~105 words)

---

## Segment 4 - Code walkthrough (2:17-4:23) · **[IDE]**

_Screen-record `Strassen\Program.cs`. Walk top to bottom; suggested scroll order below. **Before recording**, temporarily set `Threshold = 1`, and use a 4×4 or 8×8 matrix in `Main`, otherwise the 2×2 demo hits `MultiplyNaive` and never enters the Strassen branch._

> **(`Multiply`, lines ~8-50)** This is the public entry point. It checks the matrices are compatible, then finds the largest dimension and rounds it up to a power of two. Strassen needs halves all the way down, so we pad both matrices with zeros into n by n squares. At the end we copy out only the rows and columns the caller asked for. Padding is simple but it's a cost: a 65 by 65 matrix becomes 128 by 128.
>
> **(`MultiplyRecursive`, base case)** Here's the recursion. First, a base case: if n is at or below the threshold, we call plain triple-loop multiplication. In production this is set around 64 or higher, because Strassen's overhead is not worth it on small blocks. For this demo I've dropped it so we can see the real thing.
>
> **(`Slice` calls)** Next we split each matrix into the four quadrants: a11, a12, a21, a22, and the same for b. Each slice is a copy.
>
> **(the seven `m` variables)** Now the heart. These seven calls to `MultiplyRecursive` are the seven products from the slide. m1 is `Add(a11, a22)` times `Add(b11, b22)`. Count them: seven recursive calls, not eight. Notice the Add and Subtract helpers are used on the arguments, that is the extra cheap work.
>
> **(the c11..c22 lines)** Then we recombine. c11 is m1 plus m4 minus m5 plus m7, c12 is m3 plus m5, c21 is m2 plus m4, and c22 is m1 minus m2 plus m3 plus m6. Exactly the formulas we just proved.
>
> **(`Join`)** `Join` stitches the four quadrants back into one n by n result, which gets passed up the call stack.
>
> **(`Main`)** And running it on a small example: the answer matches the classical product. The helpers `Add`, `Subtract`, `Slice`, and `Join` all allocate new arrays, so this code is clear, but memory-hungry. Real libraries reuse buffers.

(~320 words)

---

## Segment 5 - Why n^log₂7 (4:23-5:38) · **[SLIDES 5-6]**

_Slide 5: recurrence + level-by-level recursion tree table. Slide 6: comparison table._

> So why does saving one multiplication change the exponent? Write down the cost. Multiplying n by n takes seven multiplications of size n over two, plus the additions, which touch every entry a constant number of times, so that's order n-squared. T of n equals 7 T of n over 2, plus n-squared.
>
> Think of it as a tree. At level k there are 7 to the k subproblems, each of size n over 2 to the k. The tree is log base 2 of n levels deep. The additions at each level cost n-squared times seven-fourths to the k. That is a growing geometric series, so the bottom level dominates. And the bottom level has 7 to the log-two-of-n leaves, which equals n to the log-two-of-seven. That's about n to the 2.81.
>
> Compare with the classical tree: eight children per node, same depth, giving 8 to the log n, which is n-cubed. Each level saves one eighth of the work, and across log n levels that compounds. For a matrix of 1,024 by 1,024, Strassen needs about 280 million leaf multiplications versus 1.07 billion, almost four times fewer.

(~180 words)

---

## Segment 6 - Constraints and limits (5:38-6:18) · **[SLIDES 7]**

_Slide 7: two-column "when it applies" / "practical limits"._

> Where does it apply? Strassen needs subtraction, so it works over any ring: integers, reals, or arithmetic mod p. It does not work for Boolean or min-plus matrix products, where there's no subtraction to cancel terms with. Sizes must be powers of two, which we handled by padding.
>
> In practice, those eighteen extra additions per level, the extra memory, and poor cache behaviour mean it only wins for large matrices. Estimates of the crossover point have ranged from a few hundred to over a thousand, and a 2016 study found about a twenty percent gain at size 512. That's why libraries use Strassen only on the top few levels.

(~100 words)

---

## Segment 7 - Extra research and outro (6:18-7:00) · **[SLIDES 8-10]**

_Slide 8: stability table. Slide 9: omega-over-time chart. Slide 10: references (hold on screen for the final seconds)._

> Two extras I went digging for. First, numerical stability. Classical multiplication has a tight per-entry error bound, but Strassen's bound is only in terms of the matrix norm, so badly scaled inputs can lose digits. Demmel and colleagues proved fast algorithms are still stable in that norm sense, so it's a worse constant, not a disaster.
>
> Second, is seven the best possible? For two by two, yes: Hopcroft and Kerr, and Winograd, proved it in 1971. For larger blocks, DeepMind's AlphaTensor found a way to multiply four by four matrices over a two-element field using 47 products, beating the 49 you get from running Strassen twice. And the best known exponent today is below 2.3714, though those algorithms are galactic, never used in practice.
>
> One trick from 1969 that still shapes the field. Thanks for watching, sources are on screen.

(~140 words)

---

## References

### Videos

1. ByteQuest. _Strassen Algorithm Visually Explained._ YouTube. https://www.youtube.com/watch?v=2IgZuVGwEb0
2. Sagar Choudhary. _Strassen's Matrix Multiplication | Faster Matrix Multiplication Explained with Example._ YouTube. https://www.youtube.com/watch?v=cGmfchtOJi4

### Articles

3. Wikipedia. _Strassen algorithm_ (recurrence, Winograd variant, crossover estimates, Huang et al. 2016 and Dalberto 2010 findings). https://en.wikipedia.org/wiki/Strassen_algorithm
4. Wikipedia. _Computational complexity of matrix multiplication_ (history of the exponent ω). https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication
5. GeeksforGeeks. _Strassen's Matrix Multiplication._ https://www.geeksforgeeks.org/strassens-matrix-multiplication/

### Research / technical

6. Strassen, V. (1969). _Gaussian elimination is not optimal._ Numerische Mathematik 13, 354-356. https://doi.org/10.1007/BF02165411
7. Demmel, J., Dumitriu, I., Holtz, O., Kleinberg, R. (2007). _Fast matrix multiplication is stable._ Numerische Mathematik 106. https://arxiv.org/abs/math/0603207
8. Fawzi, A. et al. (2022). _Discovering faster matrix multiplication algorithms with reinforcement learning_ (AlphaTensor). Nature 610, 47-53. https://www.nature.com/articles/s41586-022-05172-4
9. Alman, J., Duan, R., Vassilevska Williams, V., Xu, Y., Xu, Z., Zhou, R. (2024). _More Asymmetry Yields Faster Matrix Multiplication._ https://arxiv.org/abs/2404.16349
10. Hopcroft, J. & Kerr, L. (1971) _On minimizing the number of multiplications necessary for matrix multiplication_, SIAM J. Appl. Math; Winograd, S. (1971) _On multiplication of 2×2 matrices_, Linear Algebra Appl. 4, 381-388. https://doi.org/10.1016/0024-3795(71)90009-7

### Images (all fetched from Wikimedia Commons, not generated)

- Volker Strassen portrait: David Eppstein, CC BY-SA 3.0, `File:Strassen_Knuth_Prize_lecture.jpg`
- Strassen algorithm diagram: Cyp, CC BY-SA 3.0, `File:Strassen_algorithm.svg`
- ω over time chart: Jochen Burghardt, CC BY-SA 4.0, `File:MatrixMultComplexity_svg.svg`

---

## Notes for the presenter

- Verified from the sources: only the two YouTube IDs above resolved via YouTube oEmbed (titles match). The Nature page blocks automated fetching, so the AlphaTensor claim (47 vs 49 products, 4×4 over GF(2)) comes from secondary sources; check the paper before recording if you want to quote it precisely.
- The existing `Main` multiplies two 2×2 matrices with `Threshold = 64`, so it never executes the Strassen branch. Change `Threshold` to 1 (or use ≥128×128 inputs) for the walkthrough.
- The code pads _rectangular_ inputs to the largest dimension squared, so it is correct but wasteful; this is mentioned in segment 4.
- Timing check: if the video runs long, trim segment 7's AlphaTensor sentence first.
