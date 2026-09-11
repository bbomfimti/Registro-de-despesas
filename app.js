class Despesa {
        constructor(ano, mes, dia, tipo, descricao, valor) {
                this.ano = ano
                this.mes = mes
                this.dia = dia
                this.tipo = tipo
                this.descricao = descricao
                this.valor = valor
        }

        validarDados() {
                for(let i in this) {
                        if(this[i] == undefined || this[i] == '' || this[i] == null) {
                                return false
                        }
                }
                return true
        }
}


// API através do Application Load Balancer
const API_URL = '/api'


async function criarDespesaAPI(despesa) {

        const response = await fetch(
                `${API_URL}/despesas`,
                {
                        method: 'POST',
                        headers: {
                                'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(despesa)
                }
        )

        if (!response.ok) {
                const erro = await response.text()
                throw new Error(erro)
        }

        return await response.json()
}


async function listarDespesasAPI() {

        const response = await fetch(
                `${API_URL}/despesas`
        )

        if (!response.ok) {
                const erro = await response.text()
                throw new Error(erro)
        }

        return await response.json()
}


async function removerDespesaAPI(id) {

        const response = await fetch(
                `${API_URL}/despesas/${id}`,
                {
                        method: 'DELETE'
                }
        )

        if (!response.ok) {
                const erro = await response.text()
                throw new Error(erro)
        }

        return await response.json()
}


async function cadastrarDespesa() {

        let ano = document.getElementById('ano')
        let mes = document.getElementById('mes')
        let dia = document.getElementById('dia')
        let tipo = document.getElementById('tipo')
        let descricao = document.getElementById('descricao')
        let valor = document.getElementById('valor')

        let despesa = new Despesa(
                ano.value,
                mes.value,
                dia.value,
                tipo.value,
                descricao.value,
                valor.value
        )


        if(despesa.validarDados()) {

                try {

                        await criarDespesaAPI(despesa)

                        document.getElementById('modal_titulo').innerHTML = 'Registro inserido com sucesso'
                        document.getElementById('modal_titulo_div').className = 'modal-header text-success'
                        document.getElementById('modal_conteudo').innerHTML = 'Despesa foi cadastrada com sucesso!'
                        document.getElementById('modal_btn').innerHTML = 'Voltar'
                        document.getElementById('modal_btn').className = 'btn btn-success'

                        $('#modalRegistraDespesa').modal('show')

                        ano.value = ''
                        mes.value = ''
                        dia.value = ''
                        tipo.value = ''
                        descricao.value = ''
                        valor.value = ''

                } catch (erro) {

                        console.error('Erro ao cadastrar despesa:', erro)

                        document.getElementById('modal_titulo').innerHTML = 'Erro na inclusão do registro'
                        document.getElementById('modal_titulo_div').className = 'modal-header text-danger'
                        document.getElementById('modal_conteudo').innerHTML = 'Não foi possível cadastrar a despesa na API.'
                        document.getElementById('modal_btn').innerHTML = 'Voltar'
                        document.getElementById('modal_btn').className = 'btn btn-danger'

                        $('#modalRegistraDespesa').modal('show')
                }

        } else {

                document.getElementById('modal_titulo').innerHTML = 'Erro na inclusão do registro'
                document.getElementById('modal_titulo_div').className = 'modal-header text-danger'
                document.getElementById('modal_conteudo').innerHTML = 'Erro na gravação, verifique se todos os campos foram preenchidos corretamente!'
                document.getElementById('modal_btn').innerHTML = 'Voltar e corrigir'
                document.getElementById('modal_btn').className = 'btn btn-danger'

                $('#modalRegistraDespesa').modal('show')
        }
}


async function carregaListaDespesas(despesas = Array(), filtro = false) {

        try {

                if(despesas.length == 0 && filtro == false) {
                        despesas = await listarDespesasAPI()
                }


                let listaDespesas = document.getElementById("listaDespesas")

                listaDespesas.innerHTML = ''


                despesas.forEach(function(d) {

                        var linha = listaDespesas.insertRow()


                        linha.insertCell(0).innerHTML = `${d.dia}/${d.mes}/${d.ano}`


                        switch(d.tipo) {

                                case '1':
                                        d.tipo = 'Alimentação'
                                        break

                                case '2':
                                        d.tipo = 'Educação'
                                        break

                                case '3':
                                        d.tipo = 'Lazer'
                                        break

                                case '4':
                                        d.tipo = 'Saúde'
                                        break

                                case '5':
                                        d.tipo = 'Transporte'
                                        break
                        }


                        linha.insertCell(1).innerHTML = d.tipo
                        linha.insertCell(2).innerHTML = d.descricao
                        linha.insertCell(3).innerHTML = d.valor


                        let btn = document.createElement('button')

                        btn.className = 'btn btn-danger'
                        btn.innerHTML = '<i class="fa fa-times"></i>'
                        btn.id = `id_despesa_${d.id}`


                        btn.onclick = async function() {

                                let id = this.id.replace('id_despesa_','')

                                try {

                                        await removerDespesaAPI(id)

                                        window.location.reload()

                                } catch (erro) {

                                        console.error('Erro ao remover despesa:', erro)

                                        alert('Não foi possível remover a despesa.')

                                }
                        }


                        linha.insertCell(4).append(btn)

                        console.log(d)
                })


        } catch (erro) {

                console.error('Erro ao carregar despesas:', erro)

        }
}


async function pesquisarDespesa() {

        let ano = document.getElementById("ano").value
        let mes = document.getElementById("mes").value
        let dia = document.getElementById("dia").value
        let tipo = document.getElementById("tipo").value
        let descricao = document.getElementById("descricao").value
        let valor = document.getElementById("valor").value


        let despesa = new Despesa(
                ano,
                mes,
                dia,
                tipo,
                descricao,
                valor
        )


        try {

                let despesas = await listarDespesasAPI()


                if(despesa.ano != '') {
                        despesas = despesas.filter(d => d.ano == despesa.ano)
                }

                if(despesa.mes != '') {
                        despesas = despesas.filter(d => d.mes == despesa.mes)
                }

                if(despesa.dia != '') {
                        despesas = despesas.filter(d => d.dia == despesa.dia)
                }

                if(despesa.tipo != '') {
                        despesas = despesas.filter(d => d.tipo == despesa.tipo)
                }

                if(despesa.descricao != '') {
                        despesas = despesas.filter(d => d.descricao == despesa.descricao)
                }

                if(despesa.valor != '') {
                        despesas = despesas.filter(d => d.valor == despesa.valor)
                }


                this.carregaListaDespesas(despesas, true)


        } catch (erro) {

                console.error('Erro ao pesquisar despesas:', erro)

        }
}