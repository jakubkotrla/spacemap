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
        /// <summary>
        /// statter.exe - computes mean, min and max values in data files
        /// 
        /// INPUT: CSV file
        /// OUTPUT: CSV file
        /// 
        /// 
        /// For input file data-elnode-status.txt:
        ///  step ; node-index ; distMoved ; usage ; AGamount
        /// ouput file data-elnode-status.stats.txt: 
        ///  step ; meanDistMoved ; minDistMoved ; maxDistMoved ; meanUsage ; minUsage ; maxUsage ; meanAGamount ; minAGamount ; maxAGamount
        ///
        /// For input file data-place-status.txt:
        ///  place-index ; x ; y ; level ; range ; AGamount ; totalAGamount ; slowAGamount
        /// ouput file data-places-status.stats.txt: 
        ///  step ; meanAGamount ; minAGamount ; maxAGamount
        ///  
        /// </summary>
        static void Main(string[] args)
        {
            string fileName = String.Empty;
            if (args.Length < 1)
            {
                Program.recursiveProcess(Directory.GetCurrentDirectory());
            }
            else
            {
                fileName = args[0];
                Program.ProcessFileNode(fileName);
            }
        }

        static void recursiveProcess(string dir)
        {
            string fileNameNode = "data-elnode-status.txt";
            string fileNamePlace = "data-place-status.txt";
            string[] files = Directory.GetFiles(dir);
            foreach (string f in files)
            {
                if (Path.GetFileName(f) == fileNameNode)
                {
                    Console.WriteLine(f);
                    Program.ProcessFileNode(f);
                }
                if (Path.GetFileName(f) == fileNamePlace)
                {
                    Console.WriteLine(f);
                    Program.ProcessFilePlace(f);
                }
            }
            string[] dirs = Directory.GetDirectories(dir);
            foreach (string d in dirs)
            {
                Program.recursiveProcess(d);
            }

        }

        static void ProcessFileNode(string fileName)
        {
            TextReader tr = new StreamReader(fileName);
            string outFile = Path.GetDirectoryName(fileName);
            StreamWriter sw = new StreamWriter(Path.Combine(outFile, "data-elnode-status.stats.txt"), false);

            CsvReader csv = new CsvReader(tr, false, ';');
            int fieldCount = csv.FieldCount;

            int step = 0;
            int nodeCount = 0;
            double distSum = 0;
            double distMin = 0;
            double distMax = 0;
            double usageSum = 0;
            double usageMin = 0;
            double usageMax = 0;
            double agSum = 0;
            double agMin = 0;
            double agMax = 0;
            StringBuilder sb = new StringBuilder();
            Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US", false);

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
                    sb.Append(distMin);
                    sb.Append(";");
                    sb.Append(distMax);
                    sb.Append(";");
                    sb.Append(usageMean);
                    sb.Append(";");
                    sb.Append(usageMin);
                    sb.Append(";");
                    sb.Append(usageMax);
                    sb.Append(";");
                    sb.Append(agMean);
                    sb.Append(";");
                    sb.Append(agMin);
                    sb.Append(";");
                    sb.Append(agMax);

                    sw.WriteLine(sb.ToString());

                    step = stepRead;
                    nodeCount = 0;
                    distSum = 0;
                    distMin = 0;
                    distMax = 0;
                    usageSum = 0;
                    usageMin = 0;
                    usageMax = 0;
                    agSum = 0;
                    agMax = double.MinValue;
                    agMin = double.MaxValue;
                }

                nodeCount++;
                double distRead = double.Parse(csv[2]);
                double usageRead = double.Parse(csv[3]);
                double agRead = double.Parse(csv[4]);

                distSum += distRead;
                distMin = Math.Min(distMin, distRead);
                distMax = Math.Max(distMax, distRead);
                usageSum += usageRead;
                usageMin = Math.Min(usageMin, usageRead);
                usageMax = Math.Max(usageMax, usageRead);
                agSum += agRead;
                agMin = Math.Min(agMin, agRead);
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
            sb.Append(distMin);
            sb.Append(";");
            sb.Append(distMax);
            sb.Append(";");
            sb.Append(usageMean);
            sb.Append(";");
            sb.Append(usageMin);
            sb.Append(";");
            sb.Append(usageMax);
            sb.Append(";");
            sb.Append(agMean);
            sb.Append(";");
            sb.Append(agMin);
            sb.Append(";");
            sb.Append(agMax);

            sw.WriteLine(sb.ToString());

            tr.Close();
            sw.Close();
        }

        static void ProcessFilePlace(string fileName)
        {
            StreamReader tr = new StreamReader(fileName);
            string outFile = Path.GetDirectoryName(fileName);
            StreamWriter sw = new StreamWriter(Path.Combine(outFile, "data-places-status.stats.txt"), false);
            
            CsvReader csv = new CsvReader(tr, false, ';');
            int fieldCount = csv.FieldCount;

            int step = 0;
            int nodeCount = 0;
            double agSum = 0;
            double agMin = 0;
            double agMax = 0;
            StringBuilder sb = new StringBuilder();
            Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US", false);

            double agMean;

            while (csv.ReadNextRecord())
            {
                //line: step ; index ; x ; y ; level ; range ; AG ; totalAG ; slowAG
                int stepRead = int.Parse(csv[0]);

                if ((step != stepRead) || csv.EndOfStream)
                {
                    agMean = agSum / nodeCount;

                    sb.Length = 0;
                    sb.Append(step);
                    sb.Append(";");
                    sb.Append(agMean);
                    sb.Append(";");
                    sb.Append(agMin);
                    sb.Append(";");
                    sb.Append(agMax);

                    sw.WriteLine(sb.ToString());

                    step = stepRead;
                    nodeCount = 0;
                    agSum = 0;
                    agMax = double.MinValue;
                    agMin = double.MaxValue;
                }

                nodeCount++;
                double agRead = double.Parse(csv[6]);

                agSum += agRead;
                agMin = Math.Min(agMin, agRead);
                agMax = Math.Max(agMax, agRead);
            }
            agMean = agSum / nodeCount;

            sb.Length = 0;
            sb.Append(step);
            sb.Append(";");
            sb.Append(agMean);
            sb.Append(";");
            sb.Append(agMin);
            sb.Append(";");
            sb.Append(agMax);

            sw.WriteLine(sb.ToString());

            tr.Close();
            sw.Close();

            //distribute to files
            string outDir = Path.Combine(outFile, "places\\");
            Directory.CreateDirectory(outDir);
            Dictionary<int, StreamWriter> outFiles = new Dictionary<int, StreamWriter>();

            tr = new StreamReader(fileName);
            while(! tr.EndOfStream)
            {
                string line = tr.ReadLine();
                string[] fs = line.Split(';');
                int index = int.Parse( fs[1] );

                if (!outFiles.ContainsKey(index))
                {
                    outFiles[index] = new StreamWriter(Path.Combine(outDir, "place-" + index + ".txt"));
                }
                outFiles[index].WriteLine(line);
            }
            tr.Close();
            foreach (StreamWriter of in outFiles.Values)
            {
                of.Close();
            }
        }
        
    }
}
