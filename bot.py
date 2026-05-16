import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ARQUIVO = "dados_estudos.json"


# -------------------------
# Funções de banco JSON
# -------------------------
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {"tarefas": [], "provas": [], "materias": []}
    with open(ARQUIVO, "r") as f:
        return json.load(f)


def salvar_dados(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)


# -------------------------
# Evento inicial
# -------------------------
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


# -------------------------
# Adicionar tarefa
# -------------------------
@bot.command()
async def tarefa(ctx, *, descricao):
    dados = carregar_dados()
    dados["tarefas"].append(descricao)
    salvar_dados(dados)

    await ctx.send(f"📌 Tarefa adicionada: {descricao}")


# -------------------------
# Listar tarefas
# -------------------------
@bot.command()
async def tarefas(ctx):
    dados = carregar_dados()

    if not dados["tarefas"]:
        await ctx.send("✅ Nenhuma tarefa cadastrada.")
        return

    lista = "\n".join(
        [f"{i+1}. {t}" for i, t in enumerate(dados["tarefas"])]
    )

    await ctx.send(f"📚 Suas tarefas:\n{lista}")


# -------------------------
# Adicionar matéria
# -------------------------
@bot.command()
async def materia(ctx, *, nome):
    dados = carregar_dados()
    dados["materias"].append(nome)
    salvar_dados(dados)

    await ctx.send(f"📖 Matéria adicionada: {nome}")


# -------------------------
# Listar matérias
# -------------------------
@bot.command()
async def materias(ctx):
    dados = carregar_dados()

    if not dados["materias"]:
        await ctx.send("📭 Nenhuma matéria cadastrada.")
        return

    lista = "\n".join(
        [f"{i+1}. {m}" for i, m in enumerate(dados["materias"])]
    )

    await ctx.send(f"📝 Matérias:\n{lista}")


# -------------------------
# Agendar prova
# -------------------------
@bot.command()
async def prova(ctx, materia, data):
    dados = carregar_dados()

    dados["provas"].append({
        "materia": materia,
        "data": data
    })

    salvar_dados(dados)

    await ctx.send(f"🗓️ Prova de {materia} marcada para {data}")


# -------------------------
# Listar provas
# -------------------------
@bot.command()
async def provas(ctx):
    dados = carregar_dados()

    if not dados["provas"]:
        await ctx.send("🎉 Nenhuma prova agendada.")
        return

    lista = "\n".join(
        [f"{i+1}. {p['materia']} - {p['data']}" for i, p in enumerate(dados["provas"])]
    )

    await ctx.send(f"📅 Provas agendadas:\n{lista}")


# -------------------------
# Rodar bot
# -------------------------
bot.run("SEU_TOKEN_AQUI")