#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<vector>

using namespace std;
int main()
{
	//读取comp部分可用评分词
	ifstream tin("temp1.txt");
	if (!tin.is_open())
	{
		cout << "NOT OPEN!" << endl;
		return -1;
	}

	string comp[20];
	int compgrade[20];
	int indexComp = 0;
	string tmp;
	int n = 0;
	while (getline(tin, tmp))
	{
		istringstream is(tmp);
		string field;
		while (getline(is, field, ' '))
		{
			if (n % 2 == 0)
			{
				comp[indexComp] = field;
				//cout<<"comp:"<< field << endl;
			}
			if (n % 2 == 1)
			{
				compgrade[indexComp++] = stoi(field);
				//cout<<"num:" << field << endl;
			}
			n++;
		}
	}
	tin.close();

	//读取abs部分可用评分词
	ifstream tin1("p1to5.csv");
	if (!tin1.is_open())
	{
		cout << "NOT OPEN!" << endl;
		return -1;
	}
	string abs[50];
	int absgrade[50];
	int indexAbs = 0;
	string s;
	n = 0;
	getline(tin1, s);
	while (getline(tin1, s))
	{
		istringstream is(s);
		string field;
		while (getline(is, field, ','))
		{
			if (n % 2 == 0)
			{
				abs[indexAbs] = field;
				//cout << "comp:" << field << endl;
			}
			if (n % 2 == 1)
			{
				absgrade[indexAbs++] = stoi(field);
				//cout << "num:" << field << endl;
			}
			n++;
		}
	}
	tin1.close();

	ifstream fin("bugs.csv");

	vector<string> compInBug;
	string abstInBug[9200];
	int oldRank[9200];
	int newRank[9200];
	int numOfBugs = 0;

	if(!fin.is_open())
	{
		cout << "NOT OPEN!" << endl;
		return -1;
	}
	string line;
	getline(fin, line);
	while (getline(fin, line))
	{
		istringstream is(line);
		vector<string> fields;
		string field; 
		while (getline(is, field, ','))
		{
			fields.push_back(field);
		}
		//cout << fields[2] << endl << fields[3] << endl;
		//cout << numOfBugs<<": "<<fields[4].substr(1, 1) << endl;
		compInBug.push_back(fields[2]);
		abstInBug[numOfBugs]=fields[3];
		oldRank[numOfBugs]=stoi(fields[4].substr(1, 1));
		numOfBugs++;
	}
	//cout << "------------------" << endl;
	//cout << "numofbugs" << numOfBugs<<endl;
	//cout<<compInBug[numOfBugs-1]<<endl<<abstInBug[numOfBugs-1]<<endl;
	//每一项Bug的分数
	int *grade = new int[numOfBugs];
	for (int i = 0; i < numOfBugs; i++)
	{
		grade[i] = 0;
	}

	//用Comp对Bug评分
	for (int i = 0; i < indexComp; i++)
	{
		for (int j = 0; j < numOfBugs; j++)
		{
			string c = compInBug[j];
			if (c == comp[i])
			{
				grade[j] += compgrade[i];
			}
		}
	}

	//用Abst给Bug评分
	for (int i = 0; i < indexAbs; i++)
	{
		for (int j = 0; j < numOfBugs; j++)
		{
			string s = abstInBug[j];
			size_t pos = s.find(abs[i]);
			if (pos != s.npos)
			{
				grade[j] += absgrade[i];
			}
		}
	}

	fin.close();

	ofstream out("result.csv");
	for (int i = 0; i < numOfBugs; i++)
	{
		if (grade[i] >= 8)
		{
			newRank[i] = 1;
		}
		else if (grade[i] >= 6)
		{
			newRank[i] = 2;
		}
		else if (grade[i] >= 2)
		{
			newRank[i] = 3;
		}
		else if (grade[i] >= 1)
		{
			newRank[i] = 4;
		}
		else if (grade[i] >= 0)
		{
			newRank[i] = 5;
		}
		int flag = 0;
		if (newRank[i] == oldRank[i]) flag = 1;
		out << grade[i] << "," << newRank[i] << "," << oldRank[i] <<","<< flag << endl;
	}
	out.close();
	return 0;
}