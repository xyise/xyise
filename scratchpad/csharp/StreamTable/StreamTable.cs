namespace StreamTable;
public class StreamTable
{
    public const char NoQuote = '\u0000', UseDefaultQuote = '\u0001';

    public static char DefaultQuote(char dlm)
    {
        return dlm == ',' ? '"' : NoQuote;
    }

    public static IEnumerable<string> ListFieldNames<T>()
    {
        return typeof(T).GetFields().Select(fld => fld.GetRawConstantValue().ToString());
    }
}
