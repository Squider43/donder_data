using System;
using System.Linq;
class Program
{
  static void Main(string[] args)
  {
    int[] nm = Console.ReadLine().Split(" ").Select(int.Parse).ToArray();//傷薬の数、体力、目標体力
    int[] portion = Console.ReadLine().Split(" ").Select(int.Parse).ToArray();//portionそれぞれの回復量
    Console.WriteLine(nm[0]);
    int i = 0;//ポーションの数−１
    int dif = nm[2] - nm[0];//差分
    while(true)
    {
      if(dif <= portion[i])//差分に対してポーションの回復量が上回っていたらtrue
      {
        i++;
        break;
      }
      i++;
    }
    Console.WriteLine(i);
  }
}
