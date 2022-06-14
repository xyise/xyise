using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace BSplineFunc;
public enum CubicSplineBoundaryCondition { None, C1Flat, C2Flat }
public static class BSpline
{

    public static double basisFunc(double[] knots, double t)
    {

        // this is a recursive function

        if (knots.Length == 2)
        {
            if (t >= knots[0] && t < knots[1])
                return 1.0; 
            else
                return 0.0;
        }
        else
        {
            int nK = knots.Length - 1;
            double[] knots_i = knots.Take(nK).ToArray();
            double[] knots_ip1 = knots.Skip(1).ToArray();

            double ti_i = knots_i[0];
            double tikm1_i = knots_i[nK - 1];
            double w_i_k = ti_i < tikm1_i ? (t - ti_i) / (tikm1_i - ti_i) : 0.0;

            double ti_ip1 = knots_ip1[0];
            double tikmp1_ip1 = knots_ip1[nK - 1];
            double w_ip1_k = ti_ip1 < tikmp1_ip1 ? (t - ti_ip1) / (tikmp1_ip1 - ti_ip1) : 0.0;

            // recursion
            return w_i_k * basisFunc(knots_i, t) + (1.0 - w_ip1_k) * basisFunc(knots_ip1, t);
        }
    }

    public static double [] GetEstimateFromRegressedCurve(double[] targetOrds, double[] knotsAll, double[] alphas, int splineOrder)
    {
        double[,] bFunc = CreateAllBaseFunc(knotsAll, splineOrder, targetOrds);
        double[] results = new double[bFunc.GetLength(0)];
        for (int i = 0; i < bFunc.GetLength(0); ++i)
        {
            double temp = 0.0;
            for (int j = 0; j < bFunc.GetLength(1); ++j)
            {
                temp += bFunc[i, j] * alphas[j];
            }
            results[i] = temp;

        }
        return results; 
    }

    public static double[,] CreateAllBaseFunc(double[] knotsExtended, int order, double[] ords)
    {
        // need (order+1) knots. e.g. 
        // order=2 => need three knots (triangle)
        // order=3 => 4 knots (quadratic)
        // order=4 => 5 knots (cubic)

        int numBaseFunc = knotsExtended.Length - order;
        int numKnotsAtThisOrder = order + 1;
        double[,] allBaseFuncMatrix = new double[ords.Length, numBaseFunc];
        for (int i = 0; i < numBaseFunc; ++i)
        {
            double[] currKnots = knotsExtended.Take(i + numKnotsAtThisOrder).Skip(i).ToArray();
            for (int j = 0; j < ords.Length; ++j)
                allBaseFuncMatrix[i,j] = basisFunc(currKnots, ords[j]);
        }
        return allBaseFuncMatrix;
    }

    public static double[,] CreateAllCubicSplineBaseFuncWithBoundaryConditions(
        double[] knotsOriginal,
        double[] ords,
        CubicSplineBoundaryCondition leftBdryCond = CubicSplineBoundaryCondition.C2Flat, 
        CubicSplineBoundaryCondition rightBdryCond = CubicSplineBoundaryCondition.C2Flat
    )
    {
        int order = 4; // because we are concerned with cubic spline

        double kFirst = knotsOriginal.First();
        double kLast = knotsOriginal.Last();
        double knotsWidth = kLast - kFirst;

        double rLarge = Math.Max(1.0, knotsWidth) * 1.0e32; // this is hard coded.. ideally, the multiplication factor should be defined elsewhere

        double[] knotsFullExt = new double[] { -rLarge + kFirst, kFirst, kFirst }
                                    .Concat(knotsOriginal)
                                    .Concat(new double[] { kLast, kLast, kLast + rLarge }).ToArray();

        double[,] allBaseFuncMatrix = CreateAllBaseFunc(knotsFullExt, order, ords);
        int nords = ords.Length;
        int nBaseFunc = allBaseFuncMatrix.GetLength(1);

        double[][] allBaseFuncArrays = Utils.ArrayHelper.ToJagged2D(allBaseFuncMatrix);

        if (leftBdryCond == CubicSplineBoundaryCondition.C1Flat)
        {
            for (int j = 0; j < nords; ++j)
                allBaseFuncArrays[1][j] = allBaseFuncArrays[0][j] + allBaseFuncArrays[1][j];
        }
        else if (leftBdryCond == CubicSplineBoundaryCondition.C2Flat)
        {
            double width01 = knotsOriginal[1] - knotsOriginal[0];
            double[] xL = new double[] { 0.2, 0.4, 0.6, 0.8 }.Select(x => x * width01).ToArray();
            double[][] allBaseFunc_xL = Utils.ArrayHelper.ToJagged2D(
                CreateAllBaseFunc(knotsFullExt.Select(v => v - kFirst).ToArray(), order, xL));

            double c0 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[0], order - 1)[2];
            double c1 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[1], order - 1)[2];
            double c2 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[2], order - 1)[2];

            for (int j = 0; j < nords; ++j)
            {
                allBaseFuncArrays[1][j] = -c0 / c1 * allBaseFuncArrays[1][j] + allBaseFuncArrays[0][j];
                allBaseFuncArrays[2][j] = allBaseFuncArrays[2][j] - c2 / c0 * allBaseFuncArrays[0][j]
                                            + c2 / c0 * allBaseFuncArrays[1][j];

            }
        } // end of else if. // else = None => nothing to do

        // now right boundary
        if (rightBdryCond == CubicSplineBoundaryCondition.C1Flat)
        {
            for (int j = 0; j < nords; ++j)
                allBaseFuncArrays[nBaseFunc - 2][j] = allBaseFuncArrays[nBaseFunc - 1][j] + allBaseFuncArrays[nBaseFunc - 2][j];
        }
        else if (rightBdryCond == CubicSplineBoundaryCondition.C2Flat)
        {
            int kCount = knotsOriginal.Length;
            double width01 = knotsOriginal[kCount - 1] - knotsOriginal[kCount - 2];
            double[] xL = new double[] { 0.2, 0.4, 0.6, 0.8 }.Select(x => -x * width01).ToArray();
            double[][] allBaseFunc_xL = Utils.ArrayHelper.ToJagged2D(
                CreateAllBaseFunc(knotsFullExt.Select(v => v - kLast).ToArray(), order, xL));

            int P = allBaseFunc_xL.Length - 2;

            double cPp1 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[P + 1], order - 1)[2];
            double cP0 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[P], order - 1)[2];
            double cPn1 = MathNet.Numerics.Fit.Polynomial(xL, allBaseFunc_xL[P - 1], order - 1)[2];

            for (int j = 0; j < nords; ++j)
            {
                allBaseFuncArrays[P][j] = -cPp1 / cP0 * allBaseFuncArrays[P][j] + allBaseFuncArrays[P + 1][j];
                allBaseFuncArrays[P - 1][j] = allBaseFunc_xL[P - 1][j] - cPn1 / cPp1 * allBaseFuncArrays[P + 1][j]
                                            + cPn1 / cPp1 * allBaseFuncArrays[P][j];
            }
        }

        int leftSkip = leftBdryCond == CubicSplineBoundaryCondition.None ? 0 : 1;
        int rightSkip = rightBdryCond == CubicSplineBoundaryCondition.None ? 0: 1;
        int numToTake = allBaseFuncArrays.Length - leftSkip - rightSkip;

        return Utils.ArrayHelper.ToArray2D(allBaseFuncArrays.Skip(leftSkip).Take(numToTake).ToArray());
    }

}
