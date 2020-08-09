namespace ConsoleTest
{
    class Program
    {
        public static void Main(string[] args)
        {
            ReadText();
        }

        private static void ReadText()
        {
            var files = File.ReadAllLines("C:\\Users\\EDZ\\Desktop\\area.txt");
            if (files.Length > 0)
            {
                var provinces = new List<string>();
                var citys = new List<string>();
                var areas = new List<string>();
                foreach (var file in files)
                {
                    var strs = file.Trim().Split(' ');
                    if (strs.Length > 1)
                    {
                        if (strs[0].Substring(2, 4) == "0000")
                        {
                            provinces.Add(file.Trim());
                        }
                        if (strs[0].Substring(2, 4) != "0000" && strs[0].Substring(4, 2) == "00")
                        {
                            citys.Add(file.Trim());
                        }
                        if (strs[0].Substring(2, 4) != "0000" && strs[0].Substring(4, 2) != "00")
                        {
                            areas.Add(file.Trim());
                        }
                    }
                }

                var sb = new StringBuilder();
                var list = new List<object>();

                var addresslist = new List<address>();
                foreach (var province in provinces)
                {
                    var strs1 = province.Split(' ');
                    addresslist.Add(new address
                    {
                        value = strs1[0],
                        label = strs1[1],
                        children = new List<address>()
                    });
                }
                foreach (var province in provinces)
                {
                    var strs1 = province.Split(' ');

                    var clist = citys.FindAll(x => x.Substring(0, 2).Equals(province.Substring(0, 2)));
                    if (clist.Count > 0)
                    {
                        foreach (var city in clist)
                        {
                            var strs2 = city.Split(' ');
                            var address1 = addresslist.Find(x => x.value.Equals(strs1[0]));
                            if (address1 != null)
                            {
                                address1.children.Add(new address { value = strs2[0], label = strs2[1], children = new List<address>() });
                            }
                            var alist = areas.FindAll(x => x.Substring(0, 4).Equals(city.Substring(0, 4)));
                            foreach (var area in alist)
                            {
                                var strs3 = area.Split(' ');
                                var address = address1.children.Find(x => x.value.Equals(strs2[0]));
                                if (address != null)
                                {
                                    address.children.Add(new address { value = strs3[0], label = strs3[1] });
                                }
                            }
                        }
                    }
                    else
                    {
                        var alist = areas.FindAll(x => x.Substring(0, 3).Equals(province.Substring(0, 3)));
                        foreach (var area in alist)
                        {
                            var strs3 = area.Split(' ');
                            list.Add(new { value = strs1[0], label = strs1[1] });
                            var address = addresslist.Find(x => x.value.Equals(strs1[0]));
                            if (address != null)
                            {
                                address.children.Add(new address { value = strs3[0], label = strs3[1] });
                            }
                        }
                    }
                }

                sb.AppendLine("");
                sb.AppendLine("[");
                foreach (var items in addresslist)
                {
                    sb.AppendLine("{");
                    sb.AppendLine("\"label\":\"" + items.label.Trim() + "\",");
                    if (items.children != null && items.children.Count > 0)
                    {
                        sb.AppendLine("\"value\":\"" + items.value.Trim() + "\",");
                    }
                    else
                    {
                        sb.AppendLine("\"value\":\"" + items.value.Trim() + "\"");
                    }                    
                    if (items.children != null && items.children.Count > 0)
                    {
                        sb.AppendLine("\"children\":[");
                        foreach (var item in items.children)
                        {
                            sb.AppendLine("{\"label\":\"" + item.label.Trim() + "\",");
                            if (item.children != null && item.children.Count > 0)
                            {
                                sb.AppendLine("\"value\":\"" + item.value.Trim() + "\",");
                            }
                            else
                            {
                                sb.AppendLine("\"value\":\"" + item.value.Trim() + "\"");
                            }                                
                            if (item.children != null && item.children.Count > 0)
                            {
                                sb.AppendLine("\"children\":[");
                                foreach (var it in item.children)
                                {
                                    sb.AppendLine("{\"label\":\"" + it.label.Trim() + "\",");
                                    if (item.children.IndexOf(it) == item.children.Count - 1)
                                    {
                                        sb.AppendLine("\"value\":\"" + it.value.Trim() + "\"}");
                                    }
                                    else
                                    {
                                        sb.AppendLine("\"value\":\"" + it.value.Trim() + "\"},");
                                    }

                                }
                                sb.AppendLine("]");
                            }
                            
                            if (items.children.IndexOf(item) == items.children.Count - 1)
                            {
                                sb.AppendLine("}");
                            }
                            else
                            {
                                sb.AppendLine("},");
                            }
                        }
                        sb.AppendLine("]");
                    }               
                    
                    if (addresslist.IndexOf(items) == addresslist.Count - 1)
                    {
                        sb.AppendLine("}");
                    }
                    else
                    {
                        sb.AppendLine("},");
                    }
                }
                sb.AppendLine("]");
                sb.AppendLine("");
                var html = sb.ToString();
            }
        }

        public class address
        {
            public string value { get; set; }
            public string label { get; set; }

            public List<address> children { get; set; }
        }

        /// <summary>
        /// DataRow转Entity
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="r"></param>
        /// <returns></returns>
        public T DataRowToEntity<T>(DataRow r)
        {
            T t = default(T);
            t = Activator.CreateInstance<T>();
            PropertyInfo[] ps = t.GetType().GetProperties();
            foreach (var item in ps)
            {
                if (r.Table.Columns.Contains(item.Name))
                {
                    object v = r[item.Name];
                    if (v.GetType() == typeof(System.DBNull))
                        v = null;
                    item.SetValue(t, v, null);
                }
            }
            return t;
        }
    }
}