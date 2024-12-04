import { revalidatePath } from "next/cache";


export default async function Users() {

    const datasets = ["helical-ai/yolksac_human", "InstaDeepAI/nucleotide_transformer_downstream_tasks", "InstaDeepAI/nucleotide_transformer_downstream_tasks_revised"]
    const models = ["classification", "geneformer", "hyena_dna", "scgpt", "uce"]
    const applications = ["Quick-Start-Tutorial", "Cell-Type-Annotation", "Cell-Type-Classification-Fine-Tuning", "Geneformer-vs-UCE", "Hyena-DNA-Inference"]


    async function triggerDag(formData: FormData) {
        "use server";
        const dataset = formData.get("dataset");
        const model = formData.get("model");
        const application = formData.get("application");



        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");

        const username = 'airflow';
        const password = 'airflow';

        // Encode the credentials in Base64
        const base64Credentials = Buffer.from(`${username}:${password}`).toString('base64');
        const basicAuth = `Basic ${base64Credentials}`;

        // Append the Authorization header
        myHeaders.append('Authorization', basicAuth);
        const raw = JSON.stringify({
            "conf": {"dataset":dataset,"model":model, "application":application}
        });

        const requestOptions = {
            method: "POST",
            headers: myHeaders,
            body: raw
        };
        const airflowServiceUrl = process.env.AIRFLOW_WEB_SERVICE_URL || 'http://airflow-webserver:8080';
        const res = await fetch(`${airflowServiceUrl}/api/v1/dags/airflow_docker_operator/dagRuns`, requestOptions);
        const result = await res.json();
        console.log(result);
        revalidatePath("/dashboard");
    }

    return (
        <div className="py-10">


            <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-bold mb-6 text-gray-800">Helical pipeline creation</h2>
                <form action={triggerDag}>
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="dataset" className="block text-sm font-medium text-gray-700 mb-1">
                                Dataset
                            </label>
                            <select
                                id="dataset"
                                name="dataset"
                                className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="">Select a dataset</option>
                                {datasets.map((dataset) => (
                                    <option key={dataset} value={dataset}>
                                        {dataset}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-1">
                                Model
                            </label>
                            <select
                                id="model"
                                name="model"
                                className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="">Select a model</option>
                                {models.map((model) => (
                                    <option key={model} value={model}>
                                        {model}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label htmlFor="application" className="block text-sm font-medium text-gray-700 mb-1">
                                Application
                            </label>
                            <select
                                id="application"
                                name="application"
                                className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="">Select an application</option>
                                {applications.map((application) => (
                                    <option key={application} value={application}>
                                        {application}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="mt-6">
                        <button type="submit" className="w-full">
                            Create pipeline
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
