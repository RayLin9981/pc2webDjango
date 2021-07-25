
import java.util.Scanner;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author yuzhin
 */
public class Q2 {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int k = 10;
        while (true) {
            k = input.nextInt();
            if (k == 0) {
                break;
            }
            int i = 2;
            while(k > 1){
                while(k%i==0){
                    if( k/i >= i)
                        System.out.print(i+", ");
                    else
                        System.out.println(i);
                    k = k /i;
                
                }
                i++;
            
            
            }
            
            
        }

    }

}
