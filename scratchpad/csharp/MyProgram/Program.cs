// See https://aka.ms/new-console-template for more information
using StreamTable;
using BSplineFunc;

namespace MyProgram;

class MyProgram
{
    static void Main()
    {
        // Test_StreamReader(); 
        Test_BSpline();

    }

    static void Test_BSpline()
    {
        double[] knots_all = new double[] { 1.0, 3.0, 5.0, 7.0, 10.0 };
        double ord = 1.5;

        double bval = BSpline.basisFunc(knots_all, ord);

        Console.WriteLine("Hello BSpline " + bval.ToString());
    }


    static void Test_StreamReader()
    {
        string file_path = "sample_csv.csv";
        using (var sIn = new StreamReader(file_path))
        {
            using (var tblIn = new StreamTableReader(sIn, ',')){
                while (!tblIn.EndOfTable)
                {
                    using(var flds = tblIn.ReadRow())
                    {
                        foreach(var kv in flds)
                        {
                            Console.WriteLine(kv.Key + " " + kv.Value + "\n");
                        }
                    }
                }
            
            }
        }

        using (var sIn = new StreamReader(file_path))
        using (var tblIn = new StreamTableReader(sIn, ','))
            foreach(var flds in tblIn.ReadToEnd())
            {
                Console.WriteLine("one");
                Console.WriteLine(flds.ToString());
            }
    }
}

