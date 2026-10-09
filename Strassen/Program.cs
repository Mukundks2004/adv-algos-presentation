using System;

public static class Strassen
{
    private const int Threshold = 64;

    public static int[,] Multiply(int[,] a, int[,] b)
    {
        if (a == null || b == null)
            throw new ArgumentNullException(
                "Matrices cannot be null.");

        int rowsA = a.GetLength(0);
        int colsA = a.GetLength(1);
        int rowsB = b.GetLength(0);
        int colsB = b.GetLength(1);

        if (colsA != rowsB)
            throw new ArgumentException(
                "Incompatible matrix dimensions.");

        int size = Math.Max(
            Math.Max(rowsA, colsA),
            Math.Max(rowsB, colsB));

        // Pad to a power of two.
        int n = 1;
        while (n < size)
            n *= 2;

        int[,] paddedA = new int[n, n];
        int[,] paddedB = new int[n, n];

        CopyInto(a, paddedA);
        CopyInto(b, paddedB);

        int[,] paddedC = MultiplyRecursive(
            paddedA, paddedB);

        // Return only the required result dimensions.
        int[,] result = new int[rowsA, colsB];

        for (int i = 0; i < rowsA; i++)
            for (int j = 0; j < colsB; j++)
                result[i, j] = paddedC[i, j];

        return result;
    }

    private static int[,] MultiplyRecursive(
        int[,] a, int[,] b)
    {
        int n = a.GetLength(0);

        // Classical multiplication for small matrices.
        if (n <= Threshold)
            return MultiplyNaive(a, b);

        int half = n / 2;

        int[,] a11 = Slice(a, 0, 0, half);
        int[,] a12 = Slice(a, 0, half, half);
        int[,] a21 = Slice(a, half, 0, half);
        int[,] a22 = Slice(a, half, half, half);

        int[,] b11 = Slice(b, 0, 0, half);
        int[,] b12 = Slice(b, 0, half, half);
        int[,] b21 = Slice(b, half, 0, half);
        int[,] b22 = Slice(b, half, half, half);

        // Strassen's seven products.
        int[,] m1 = MultiplyRecursive(
            Add(a11, a22), Add(b11, b22));

        int[,] m2 = MultiplyRecursive(
            Add(a21, a22), b11);

        int[,] m3 = MultiplyRecursive(
            a11, Subtract(b12, b22));

        int[,] m4 = MultiplyRecursive(
            a22, Subtract(b21, b11));

        int[,] m5 = MultiplyRecursive(
            Add(a11, a12), b22);

        int[,] m6 = MultiplyRecursive(
            Subtract(a21, a11), Add(b11, b12));

        int[,] m7 = MultiplyRecursive(
            Subtract(a12, a22), Add(b21, b22));

        // Combine the four result quadrants.
        int[,] c11 = Add(
            Subtract(Add(m1, m4), m5), m7);

        int[,] c12 = Add(m3, m5);

        int[,] c21 = Add(m2, m4);

        int[,] c22 = Add(
            Subtract(Add(m1, m3), m2), m6);

        int[,] c = new int[n, n];

        Join(c, c11, 0, 0);
        Join(c, c12, 0, half);
        Join(c, c21, half, 0);
        Join(c, c22, half, half);

        return c;
    }

    private static int[,] MultiplyNaive(
        int[,] a, int[,] b)
    {
        int n = a.GetLength(0);
        int[,] c = new int[n, n];

        for (int i = 0; i < n; i++)
            for (int k = 0; k < n; k++)
                for (int j = 0; j < n; j++)
                    c[i, j] += a[i, k] * b[k, j];

        return c;
    }

    private static int[,] Add(int[,] a, int[,] b)
    {
        int n = a.GetLength(0);
        int[,] c = new int[n, n];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                c[i, j] = a[i, j] + b[i, j];

        return c;
    }

    private static int[,] Subtract(int[,] a, int[,] b)
    {
        int n = a.GetLength(0);
        int[,] c = new int[n, n];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                c[i, j] = a[i, j] - b[i, j];

        return c;
    }

    private static int[,] Slice(
        int[,] matrix, int row, int col, int size)
    {
        int[,] result = new int[size, size];

        for (int i = 0; i < size; i++)
            for (int j = 0; j < size; j++)
                result[i, j] = matrix[row + i, col + j];

        return result;
    }

    private static void Join(
        int[,] destination, int[,] source,
        int row, int col)
    {
        int n = source.GetLength(0);

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                destination[row + i, col + j] = source[i, j];
    }

    private static void CopyInto(
        int[,] source, int[,] destination)
    {
        for (int i = 0; i < source.GetLength(0); i++)
            for (int j = 0; j < source.GetLength(1); j++)
                destination[i, j] = source[i, j];
    }
}

public class Program
{
    public static void Main()
    {
        int[,] a =
        {
            { 1, 2 },
            { 3, 4 }
        };

        int[,] b =
        {
            { 5, 6 },
            { 7, 8 }
        };

        int[,] result = Strassen.Multiply(a, b);

        for (int i = 0; i < result.GetLength(0); i++)
        {
            for (int j = 0; j < result.GetLength(1); j++)
                Console.Write(result[i, j] + "\t");

            Console.WriteLine();
        }
    }
}