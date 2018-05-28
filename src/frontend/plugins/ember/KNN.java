package knnimplementation;

import java.util.Scanner;
import java.util.StringTokenizer;
/**
 *
 * @author Nayan
 */
public class KNN{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringTokenizer st;
        int featureCount = 0, classCount = 0, dataCount = 0;
        System.out.print("Enter the number of features: ");
        featureCount = Integer.parseInt(sc.nextLine());
        System.out.print("Enter the number of classes: ");
        classCount = Integer.parseInt(sc.nextLine());
        int classes[] = new int[classCount];
        for(int i = 0; i < classCount; ++i)
            classes[i] = 0;
        System.out.print("Enter the number of datasets: ");
        dataCount = Integer.parseInt(sc.nextLine());
        double dataSet[][] = new double[dataCount][featureCount + 2];
        System.out.println("Input data(<feature><space><feature>....<space><class>): ");
        for(int i = 0; i < dataCount; ++i) {
            st = new StringTokenizer(sc.nextLine());
            for(int j = 0; j < featureCount + 1; ++j) {
                dataSet[i][j] = Double.parseDouble(st.nextToken());
            }
        }
        System.out.print("Enter the query data features: ");
        st = new StringTokenizer(sc.nextLine());
        double q[] = new double[featureCount];
        for(int j = 0; j < featureCount; ++j) {
            q[j] = Double.parseDouble(st.nextToken());
        }            
        System.out.print("Enter the value of k: ");
        int k = 0;
        k = Integer.parseInt(sc.nextLine());
        for(int i = 0; i < dataCount; ++i) {
            double sum = 0;
            for(int j = 0; j < featureCount; ++j){
                sum += Math.pow((dataSet[i][j] - q[j]), 2.0);
            }
            dataSet[i][featureCount + 1] = Math.sqrt(sum);
            //System.out.println(dataSet[i][featureCount + 1]);
        }
        double[] temp;
        for(int i = 0; i < dataCount - 1; i++) {
            for(int j = 0; j < dataCount - i - 1; j++) {
                if(dataSet[j][featureCount + 1] > dataSet[j + 1][featureCount + 1]) {
                    temp = dataSet[j + 1];
                    dataSet[j + 1] = dataSet[j];
                    dataSet[j] = temp;
                }
            }
        }
        //for(int i = 0; i < dataCount; ++i)
            //System.out.println(Arrays.toString(dataSet[i]));
        for(int i = 0; i < k; ++i){
            classes[(int)dataSet[i][featureCount]]++;
        }
        //System.out.println(Arrays.toString(classes));
        int index = 0, max = 0;
        for(int i = 0; i < classCount; ++i) {
            if(classes[i] > max) {
                max = classes[i];
                index = i;
            }
        }
        System.out.println("The given value is in class " + index);
    }    
}
