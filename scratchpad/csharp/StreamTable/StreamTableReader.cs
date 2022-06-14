using System.Collections;
using System.Collections.ObjectModel;
using System.Diagnostics.CodeAnalysis;

namespace StreamTable; 

public interface IDisposableReadOnlyDictionary<TKey, TValue>: IReadOnlyDictionary<TKey, TValue>, IDisposable
{
    
}

public class StreamTableReader : IDisposable
{
    // private members

    private readonly char dlm; 
    private readonly IReadOnlyList<string> fldNms; 
    private readonly IReadOnlyDictionary<string, int> fldIcs;

    private readonly StreamReader sIn;
    private readonly SortedDictionary<int, string> bfr; 
    private int nxtRwIdx;



    // constructor
    public StreamTableReader(StreamReader sIn, char dlm)
    {
        this.sIn = sIn; 
        this.dlm = dlm; 

        var nxtLn = FetchNextLine();   

        this.fldNms = SplitWithQuote(nxtLn);

        var fldIcs_ = new Dictionary<string, int>(); 
        
        for (var i = 0; i < this.fldNms.Count; ++i)
        {
            fldIcs_[fldNms[i]]=i; 
        }
        this.fldIcs = fldIcs_;

        this.bfr = new SortedDictionary<int, string>(); 
        this.nxtRwIdx = -1; 
        bfr[++nxtRwIdx] = FetchNextLine();
        
    }

    private string FetchNextLine()
    {   
        return sIn.ReadLine();
    }

    public void Dispose()
    {
    }

    public IReadOnlyList<string> FieldNames{
        get { return this.fldNms; }
    }

    public bool EndOfTable
    {
        get { 
            lock(sIn)
            return bfr.Values.First() == null; 

        }
    }

    public IDisposableReadOnlyDictionary<string, string> ReadRow()
    {
        lock (sIn)
        {            
            int idx = bfr.Keys.First(); 
            if (nxtRwIdx < idx || bfr[idx] == null)
                throw new Exception("exhausted");
            
            var fldVals = Array.AsReadOnly(SplitWithQuote(bfr[idx]));
            bfr.Remove(idx);
            if (nxtRwIdx == idx)
                bfr[++nxtRwIdx] = FetchNextLine();
            return new RowReader(fldIcs, fldVals);
        }

    }

    private string[] SplitWithQuote(string s)
    {
        return s.Split(dlm);
    }

    class RowReader : IDisposableReadOnlyDictionary<string, string>
    {
        private IReadOnlyDictionary<string, int> fldIdcs;
        private ReadOnlyCollection<string> fldVals;

        public RowReader(IReadOnlyDictionary<string, int> fldIdcs, ReadOnlyCollection<string> fldVals)
        {
            this.fldIdcs = fldIdcs; 
            this.fldVals = fldVals;
        }

        public string this[string key] => fldVals[fldIdcs[key]]; 

        public IEnumerable<string> Keys => fldIdcs.Keys; 

        public IEnumerable<string> Values => fldVals;

        public int Count => fldIdcs.Count; 

        public bool ContainsKey(string key)
        {
            return fldIdcs.ContainsKey(key);
        }

        public void Dispose()
        {
        }

        public IEnumerator<KeyValuePair<string, string>> GetEnumerator()
        {
            return new Enumerator(fldIdcs.GetEnumerator(), fldVals);
        }

        public bool TryGetValue(string key, [MaybeNullWhen(false)] out string value)
        {

            if (fldIdcs.ContainsKey(key))
            {
                value = ((IReadOnlyDictionary<string,string>)this)[key];
                return true; 
            }
            else
            {
                value = null; 
                return false;
            }
            throw new NotImplementedException();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return new Enumerator(fldIdcs.GetEnumerator(), fldVals);
        }

        class Enumerator : IEnumerator<KeyValuePair<string, string>>, IDisposable
        {
            private IEnumerator<KeyValuePair<string, int>> enm; 
            private ReadOnlyCollection<string> fldVals; 

            public Enumerator(IEnumerator<KeyValuePair<string, int>> enm, ReadOnlyCollection<string> fldVals)
            {
                this.enm = enm; 
                this.fldVals = fldVals;
            }

            public KeyValuePair<string, string> Current => new KeyValuePair<string, string>(enm.Current.Key, fldVals[enm.Current.Value]); 

            object IEnumerator.Current => new KeyValuePair<string, string>(enm.Current.Key, fldVals[enm.Current.Value]); 

            public void Dispose()
            {
                enm.Dispose(); 
            }

            public bool MoveNext()
            {
                return enm.MoveNext(); 
            }

            public void Reset()
            {
                enm.Reset(); 
            }
        }
    }


}