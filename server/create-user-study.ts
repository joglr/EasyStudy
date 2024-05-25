#!/usr/bin/env bun
const req = await fetch("http://localhost:5000/create-user-study", {
  "headers": {
    "accept": "*/*",
    "accept-language": "da-DK,da;q=0.9,en-DK;q=0.8,en-US;q=0.7,en;q=0.6,ak;q=0.5",
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrftoken": "IjY0MDY0ZjAxMWE0NTBkZWQ0NTRiNWMyOWU2OWNkOTdhNDEyYmJhNTAi.ZvQzPw.fg84OU_f5XUElu0Enk8oeng9FYs",
    "cookie": "something=4f68ee16-7501-4f96-b643-77343e869cf2; remember_token=bob@bob|d6b5b4e52913c0d01abebb23eb6cfde289b780ed06c03dfb45cafd4f3047c5b9b4ca352c37e9b0cc3856b5ab94b37989a417b3892626927934e64cb029fb14ad",
    "Referer": "http://localhost:5000/fastcompare/create",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": "{\"parent_plugin\":\"fastcompare\",\"config\":{\"k\":10,\"prolific_code\":null,\"n_algorithms_to_compare\":2,\"result_layout\":\"rows\",\"shuffle_algorithms\":true,\"shuffle_recommendations\":true,\"algorithm_parameters\":[{\"latent\":128,\"positive_threshold\":2.5,\"epochs\":10,\"lr\":0.1,\"device\":\"cpu\",\"verbose\":true,\"displayed_name\":\"EasyStudyELSA\",\"name\":\"EasyStudyELSA\"},{\"l2\":0.1,\"positive_threshold\":2.5,\"displayed_name\":\"k-means\",\"name\":\"k-means\"}],\"n_iterations\":5,\"selected_algorithms\":[\"EasyStudyELSA\",\"k-means\"],\"selected_preference_elicitation\":\"Popularity Sampling\",\"preference_elicitation_parameters\":{\"n_samples\":10,\"k\":1},\"selected_data_loader\":\"Filtered ML-25M dataset\",\"data_loader_parameters\":{},\"text_overrides\":{\"footer\":\"\"},\"show_final_statistics\":true}}",
  "method": "POST"
});

if (!req.ok) {
  throw new Error(`HTTP error! status: ${req.status}, statusText: ${req.statusText}`);
}
