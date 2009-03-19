using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using LumenWorks.Framework.IO.Csv;
using System.IO;
using System.Globalization;
using System.Threading;

namespace statter
{
    class Program
    {
        // input: CSV file with lines: step ; node-index ; distMoved ; usage ; AGamount
        // ouput: CSV file with lines: step ; meanDistMoved ; maxDistMoved ; meanUsage ; maxUsage ; meanAGamount ; maxAGamount
        static void Main(string[] args)
        {
            string fileName = String.Empty;
            if (args.Length < 1)
            {
                fileName = "data-elnode-status.txt";
            }
            else
            {
                fileName = args[0];
            }
            TextReader tr = new StreamReader(fileName);
            StreamWriter sw = new StreamWriter("data-elnode-status.stats.txt", false);


            CsvReader csv = new CsvReader(tr, false, ';');
            int fieldCount = csv.FieldCount;

            int step = 0;
            int nodeCount = 0;
            double distSum = 0;
            double distMax = 0;
            double usageSum = 0;
            double usageMax = 0;
            double agSum = 0;
            double agMax = 0;
            StringBuilder sb = new StringBuilder();
            Thread.CurrentThread.CurrentCulture = new CultureInfo( "en-US", false );

            double distMean;
            double usageMean;
            double agMean;

            while (csv.ReadNextRecord())
            {
                //line: step ; node-index ; distMoved ; usage ; AGamount
                
                int stepRead = int.Parse(csv[0]);

                if ((step != stepRead) || csv.EndOfStream)
                {
                    distMean = distSum / nodeCount;
                    usageMean = usageSum / nodeCount;
                    agMean = agSum / nodeCount;

                    sb.Length = 0;
                    sb.Append(step);
                    sb.Append(";");
                    sb.Append(distMean);
                    sb.Append(";");
                    sb.Append(distMax);
                    sb.Append(";");
                    sb.Append(usageMean);
                    sb.Append(";");
                    sb.Append(usageMax);
                    sb.Append(";");
                    sb.Append(agMean);
                    sb.Append(";");
                    sb.Append(agMax);

                    sw.WriteLine(sb.ToString());

                    step = stepRead;
                    nodeCount = 0;
                    distSum = 0;
                    distMax = 0;
                    usageSum = 0;
                    usageMax = 0;
                    agSum = 0;
                    agMax = double.MinValue;
                }
                
                nodeCount++;
                double distRead = double.Parse(csv[2]);
                double usageRead = double.Parse(csv[3]);
                double agRead = double.Parse(csv[4]);

                distSum += distRead;
                distMax = Math.Max(distMax, distRead);
                usageSum += usageRead;
                usageMax = Math.Max(usageMax, usageRead);
                agSum += agRead;
                agMax = Math.Max(agMax, agRead);
            }
            distMean = distSum / nodeCount;
            usageMean = usageSum / nodeCount;
            agMean = agSum / nodeCount;

            sb.Length = 0;
            sb.Append(step);
            sb.Append(";");
            sb.Append(distMean);
            sb.Append(";");
            sb.Append(distMax);
            sb.Append(";");
            sb.Append(usageMean);
            sb.Append(";");
            sb.Append(usageMax);
            sb.Append(";");
            sb.Append(agMean);
            sb.Append(";");
            sb.Append(agMax);

            sw.WriteLine(sb.ToString());


            tr.Close();
            sw.Close();
        }
    }
}
