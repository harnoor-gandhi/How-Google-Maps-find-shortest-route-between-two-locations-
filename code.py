int calcDist(point &p)
{

    int x = end.x - p.x, y = end.y - p.y;
    return (x * x + y * y);
}

bool isValid(point &p)
{
    return (p.x > -1 && p.y > -1 && p.x < m.w && p.y < m.h);
}

bool existPoint(point &p, int cost)
{
    std::list<node>::iterator i;
    i = std::find(closed.begin(), closed.end(), p);
    if (i != closed.end())
    {
        if ((*i).cost + (*i).dist < cost)
            return true;
        else
        {
            closed.erase(i);
            return false;
        }
    }
    i = std::find(open.begin(), open.end(), p);
    if (i != open.end())
    {
        if ((*i).cost + (*i).dist < cost)
            return true;
        else
        {
            open.erase(i);
            return false;
        }
    }
    return false;
}

bool fillOpen(node &n)
{
    int stepCost, nc, dist;
    point neighbour;

    for (int x = 0; x < 8; x++)
    {
        stepCost = x < 4 ? 1 : 1;
        neighbour = n.pos + neighbours[x];
        if (neighbour == end)
            return true;

        if (isValid(neighbour) && m(neighbour.x, neighbour.y) != 1)
        {
            nc = stepCost + n.cost;
            dist = calcDist(neighbour);
            if (!existPoint(neighbour, nc + dist))
            {
                node m;
                m.cost = nc;
                m.dist = dist;
                m.pos = neighbour;
                m.parent = n.pos;
                open.push_back(m);
            }
        }
    }
    return false;
}

bool search(point &s, point &e, map &mp)
{
    node n;
    end = e;
    start = s;
    m = mp;
    n.cost = 0;
    n.pos = s;
    n.parent = 0;
    n.dist = calcDist(s);
    open.push_back(n);
    while (!open.empty())
    {
        node n = open.front();
        open.pop_front();
        closed.push_back(n);
        if (fillOpen(n))
            return true;
    }
    return false;
}

int path(std::list<point> &path)
{
    path.push_front(end);
    int cost = 1 + closed.back().cost;
    path.push_front(closed.back().pos);
    point parent = closed.back().parent;

    for (std::list<node>::reverse_iterator i = closed.rbegin(); i != closed.rend(); i++)
    {
        if ((*i).pos == parent && !((*i).pos == start))
        {
            path.push_front((*i).pos);
            parent = (*i).parent;
        }
    }
    path.push_front(start);
    return cost;
}

map m;
point end, start;
point neighbours[8];
std::list<node> open;
std::list<node> closed;
