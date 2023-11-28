import java.io.*;
import java.net.*;
import java.nio.file.Files;
import java.util.Base64;

public class ImageUploader {

    public static void main(String[] args) {
        String imagePath = "chemin/vers/ton/image.jpg";
        try {
            byte[] imageData = Files.readAllBytes(new File(imagePath).toPath());
            String base64Image = Base64.getEncoder().encodeToString(imageData);

            String url = "http://localhost:5000/save_image";
            URL serverUrl = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) serverUrl.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String jsonInputString = "{\"image\": \"" + base64Image + "\"}";
            try(OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            try(BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            }

            connection.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
