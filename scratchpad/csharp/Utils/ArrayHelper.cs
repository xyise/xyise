namespace Utils;
public static class ArrayHelper
{
    public static T[][] ToJagged2D<T>(T[,] array2D, bool byColumn=true)
    {
        int nR = array2D.GetLength(0);
        int nC = array2D.GetLength(1);

        int N1 = byColumn ? nC : nR;
        int N2 = byColumn ? nR : nC;

        T[][] j2d = new T[N1][];

        for (int n1 = 0; n1 < N1; ++n1)
        {
            j2d[n1] = new T[N2];
            for (int n2 = 0; n2 < N2; ++n2)
            {
                j2d[n1][n2] = byColumn ? array2D[n2, n1] : array2D[n1, n2];
            }
        }

        return j2d; 
    }

    public static T[,] ToArray2D<T>(T[][] jagged2D, bool byColumn = true)
    {
        int N1 = jagged2D.Length;
        int N2 = jagged2D[0].Length;

        int nC = byColumn ? N1 : N2;
        int nR = byColumn ? N2 : N1;

        T[,] array2D = new T[nR, nC];

        for (int r = 0; r < nR; ++r)
        {
            for (int c = 0; c < nC; ++c)
            {
                array2D[r, c] = byColumn ? jagged2D[c][r] : jagged2D[r][c];
            }
        }
        return array2D; 
    }
}
