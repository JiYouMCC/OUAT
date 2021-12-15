using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using System.Collections.Generic;

namespace Common
{
    /// <summary>
    /// Summary description for Cirque
    /// </summary>
    public class Cirque<T>
    {

        protected List<T> list = new List<T>();

        /// <summary>
        /// 获得环形队列里所有的元素
        /// </summary>
        public T[] ToArray
        {
            get
            {
                T[] ret = new T[list.Count];
                list.CopyTo(ret);
                return ret;
            }
        }

        int current = 0;

        /// <summary>
        /// 当前环形队列中指向的对象
        /// </summary>
        public T Current
        {
            get
            {
                if (list.Count > 0)
                {
                    if (current > list.Count - 1)
                        MoveLast();
                    return list[current];
                }
                return default(T);
            }
            set
            {
                int index = list.IndexOf(value);
                if (index != -1)
                    current = index;
            }
        }

        /// <summary>
        /// 队列第一个元素
        /// </summary>
        public T First
        {
            get
            {
                if (list.Count > 0)
                    return list[0];
                return default(T);
            }
        }

        /// <summary>
        /// 队列里最后一个元素
        /// </summary>
        public T Last
        {
            get
            {
                if (list.Count > 0)
                    return list[list.Count - 1];
                return default(T);
            }
        }

        /// <summary>
        /// 将环形队列指向下一个用户
        /// </summary>
        public T MoveNext()
        {
            current++;
            if (current == list.Count)
                current = 0;
            return Current;
        }

        public void MoveFirst()
        {
            current = 0;
        }

        public void MoveLast()
        {
            current = list.Count - 1;
        }

        /// <summary>
        /// 向环形队列里添加一个对象
        /// </summary>
        /// <param name="obj"></param>
        public void Add(T obj)
        {
            list.Add(obj);
        }

        /// <summary>
        /// 从环形队列里移除一个对象
        /// </summary>
        /// <param name="obj"></param>
        public void Remove(T obj)
        {
            list.Remove(obj);
        }

        /// <summary>
        /// 环形队列的对象个数
        /// </summary>
        public int Count
        {
            get
            {
                return list.Count;
            }
        }
    }

    /// <summary>
    /// 字符串列表
    /// </summary>
    public class StringList : List<string>
    {
        public override string ToString()
        {
            System.Text.StringBuilder sb = new System.Text.StringBuilder();
            foreach (string str in this)
            {
                sb.AppendLine(str);
            }
            return sb.ToString();
        }
    }
}