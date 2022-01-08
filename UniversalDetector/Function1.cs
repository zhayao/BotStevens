using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Collections.Specialized;
using System.Net;

namespace UniversalDetector
{
    public static class Function1
    {
        [FunctionName("MessagePasser")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");

            string message = req.Query["message"];

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);
            message = message ?? "You have a Push without details";

            PushNotofication(message);

            string responseMessage = string.IsNullOrEmpty(message)
                ? "Notification has been pushed but no detail message"
                : $"Message, {message} has been pushed";

            return new OkObjectResult(responseMessage);
        }


        private static string PushNotofication(string message)
        {
            var parameters = new NameValueCollection {
                    { "token", "am8uncvpxtkvu1t5kf22byctz6iymo" },
                    { "user", "u6b6soor8hrgrk4b1yaio3vbakbo1t" },
                    { "message", message}
            };

            using (var client = new WebClient())
            {
                var response = client.UploadValues("https://api.pushover.net/1/messages.json", parameters);
                return response.ToString();
            }
        }
    }
}
