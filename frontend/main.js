new Vue({
    el: '#app',
    data: {
        query: '',
        results: []
    },
    methods: {
        async search() {
            if (!this.query.trim()) {
                this.results = [];
                return;
            }

            try {
                console.log("Enviando requisição para:", `http://127.0.0.1:5000/search?q=${encodeURIComponent(this.query)}`);
                const response = await fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(this.query)}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json;charset=UTF-8'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }

                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    throw new Error("Resposta da API não é um JSON válido.");
                }

                const data = await response.json();
                console.log("Resposta da API:", data);

                if (data.error) {
                    console.error(data.error);
                    this.results = [];
                } else {
                    this.results = data;
                }
            } catch (error) {
                console.error('Erro ao buscar dados:', error);
                this.results = [];
            }
        }
    }
});
