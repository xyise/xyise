using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace MyStyleObject;

public class GenericSpreadFit
{
    public Dictionary<string, string>[] CurveMappingTable { get; private set; }
    public IEnumerable<string> CurvesToFit { get; private set; }
    public Dictionary<string, SortedSet<DateTime>> HolidaySchs { get; private set; }

    public void RunRegression()
    {
        Path.Combine("");

        Parallel.For(0, Enumerable.Range(0, 10).Select(x => 2 * x).ToArray(), null, i =>
        {
            DateTime d = new DateTime(2022, 1, 3);
        });

        foreach(var x in Enumerable.Range(0, 10))
        {
            int y = 2 * x; 
        }
        DateTime[] z;
        z = new DateTime[4];
        z[0] = new DateTime(2022, 1, 1);

        List<DateTime> dl = new List<DateTime>();
        dl.Add(new DateTime(2222, 1, 1));
        dl[0];
    }
}
