class ClassMain{
    public static void main(String[] a){
        System.out.println(new Exemplo2().metodoC(0));
    }
}

class Exemplo1{
    int e;

    public int metodoA(int a){
        int b;
        int c;
        b = 2;
        c = a + b + 167;
        return c;
    }
}

class Exemplo2{
    public int metodoC(int a){
        int[] intArray;
        int b;
        intArray = new int[20];
        intArray[0] = 1;
        if(a < 55){
            b = intArray[0];
        }
        else{
            b = 73;
        }
        return b ;
    }
}
