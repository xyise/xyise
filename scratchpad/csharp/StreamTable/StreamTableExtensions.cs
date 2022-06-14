namespace StreamTable;


public static class StreamTableExtensions
{

    public static IEnumerable<string> ReadToEnd(this StreamTableReader tbl, string fldNm)
    {
        while (!tbl.EndOfTable)
            using (var flds = tbl.ReadRow())
                yield return flds[fldNm];
    }

    public static IEnumerable<IReadOnlyDictionary<string, string>> ReadToEnd(this StreamTableReader tbl)
    {
        while (!tbl.EndOfTable)
            using (var flds = tbl.ReadRow())
                yield return flds;
    }
}