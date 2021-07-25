
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
public class Q1 {
 public static void main(String[] args){
 
 Scanner input = new Scanner(System.in);
 int times = input.nextInt();
     for (int i = 0; i < times; i++) {
         int temp = input.nextInt();
         boolean is_prime = true;
         for (int j = 2; j < (int)Math.pow(temp,0.5)+1; j++) {
             if(temp % j == 0)
                 is_prime = false;
         }
         if(is_prime)
             System.out.println("Is Prime");
         else
             System.out.println("Not Prime");
         
     }
 
 
 
 
 
 }   
}
