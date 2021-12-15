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
        /// ��û��ζ��������е�Ԫ��
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
        /// ��ǰ���ζ�����ָ��Ķ���
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
        /// ���е�һ��Ԫ��
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
        /// ���������һ��Ԫ��
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
        /// �����ζ���ָ����һ���û�
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
        /// ���ζ��������һ������
        /// </summary>
        /// <param name="obj"></param>
        public void Add(T obj)
        {
            list.Add(obj);
        }

        /// <summary>
        /// �ӻ��ζ������Ƴ�һ������
        /// </summary>
        /// <param name="obj"></param>
        public void Remove(T obj)
        {
            list.Remove(obj);
        }

        /// <summary>
        /// ���ζ��еĶ������
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
    /// �ַ����б�
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