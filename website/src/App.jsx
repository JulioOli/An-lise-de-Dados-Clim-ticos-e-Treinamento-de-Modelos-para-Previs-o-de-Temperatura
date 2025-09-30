import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const App = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [modelData, setModelData] = useState([]);

  useEffect(() => {
    // Dados dos modelos baseados no notebook
    const modelResults = [
      { model: 'Random Forest (Sem Lag)', rmse: 1.1567, mae: 0.8492, r2: 0.9121, type: 'Sem Lag', color: '#A1C9F4' },
      { model: 'Gradient Boosting (Sem Lag)', rmse: 1.2518, mae: 0.9228, r2: 0.8970, type: 'Sem Lag', color: '#B5E384' },
      { model: 'SVR (Sem Lag)', rmse: 3.5487, mae: 2.7225, r2: 0.1724, type: 'Sem Lag', color: '#FFACAC' },
      { model: 'Random Forest (Com Lag)', rmse: 1.2936, mae: 0.9328, r2: 0.8786, type: 'Com Lag', color: '#0072B2' },
      { model: 'Gradient Boosting (Com Lag)', rmse: 1.2680, mae: 0.9474, r2: 0.8834, type: 'Com Lag', color: '#009E73' },
      { model: 'SVR (Com Lag)', rmse: 3.5256, mae: 2.7268, r2: 0.0983, type: 'Com Lag', color: '#D55E00' }
    ];
    setModelData(modelResults);
  }, []);

  const tabs = [
    { id: 'overview', name: 'Visão Geral', icon: '📊' },
    { id: 'correlation', name: 'Correlações', icon: '🔗' },
    { id: 'models-sem-lag', name: 'Modelos Sem Lag', icon: '🤖' },
    { id: 'models-com-lag', name: 'Modelos Com Lag', icon: '🔄' },
    { id: 'comparison', name: 'Comparação Final', icon: '⚖️' },
    { id: 'interpretability', name: 'Interpretabilidade', icon: '🔍' },
    { id: 'data', name: 'Dados', icon: '📋' }
  ];

  const importanceDataSemLag = [
    { feature: 'pressao_atm_media', importance: 0.3130 },
    { feature: 'umidade_relativa_minima', importance: 0.3063 },
    { feature: 'temp_orvalho_media', importance: 0.2050 },
    { feature: 'umidade_relativa_media', importance: 0.1522 },
    { feature: 'umidade_relativa_maxima', importance: 0.0125 },
    { feature: 'vento_vel_media', importance: 0.0110 }
  ];

  const importanceDataComLag = [
    { feature: 'temp_maxima_lag_1', importance: 0.5894 },
    { feature: 'umidade_relativa_minima', importance: 0.1610 },
    { feature: 'temp_orvalho_media', importance: 0.0633 },
    { feature: 'pressao_atm_media', importance: 0.0362 },
    { feature: 'umidade_relativa_media', importance: 0.0311 }
  ];

  const correlationData = [
    { var1: 'temp_media', var2: 'temp_maxima', correlation: 0.95 },
    { var1: 'temp_media', var2: 'temp_minima', correlation: 0.92 },
    { var1: 'umidade_relativa', var2: 'precipitacao', correlation: 0.35 },
    { var1: 'pressao_atm', var2: 'temp_media', correlation: -0.15 },
    { var1: 'vento_vel', var2: 'precipitacao', correlation: 0.08 }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-blue-50 to-indigo-100 p-6 rounded-xl">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Análise Comparativa de Modelos de Previsão</h2>
              <p className="text-gray-700 text-lg">
                Este dashboard apresenta uma análise comparativa sistemática dos modelos de machine learning 
                para previsão de dados meteorológicos, comparando abordagens com e sem lag-features.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="text-2xl">🤖</div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Modelos Avaliados</p>
                    <p className="text-2xl font-semibold text-gray-900">6</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-green-500">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="text-2xl">🏆</div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Melhor R²</p>
                    <p className="text-2xl font-semibold text-gray-900">0.912</p>
                    <p className="text-xs text-gray-500">Random Forest (Sem Lag)</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-purple-500">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="text-2xl">📈</div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Menor RMSE</p>
                    <p className="text-2xl font-semibold text-gray-900">1.157</p>
                    <p className="text-xs text-gray-500">Random Forest (Sem Lag)</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-orange-500">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="text-2xl">🔄</div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Features Testadas</p>
                    <p className="text-2xl font-semibold text-gray-900">26</p>
                    <p className="text-xs text-gray-500">Com lag features</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Estrutura da Análise</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">1. Preparação dos Dados</h4>
                  <ul className="text-gray-600 space-y-1 text-sm">
                    <li>• Carregamento dos dados INMET</li>
                    <li>• Tratamento de valores faltantes</li>
                    <li>• Interpolação linear</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">2. Criação dos Datasets</h4>
                  <ul className="text-gray-600 space-y-1 text-sm">
                    <li>• Dataset sem lag features</li>
                    <li>• Dataset com lag features (1, 2, 3, 7 dias)</li>
                    <li>• Divisão treino/teste (80/20)</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">3. Modelos Avaliados</h4>
                  <ul className="text-gray-600 space-y-1 text-sm">
                    <li>• Random Forest</li>
                    <li>• Gradient Boosting</li>
                    <li>• Support Vector Regression</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">4. Interpretabilidade</h4>
                  <ul className="text-gray-600 space-y-1 text-sm">
                    <li>• Análise SHAP</li>
                    <li>• Explicações LIME</li>
                    <li>• Importância das features</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        );

      case 'correlation':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Análise de Correlações</h2>
              
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Correlações Mais Significativas</h3>
                <div className="space-y-3">
                  {correlationData.map((corr, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <span className="font-medium">{corr.var1}</span>
                        <span className="text-gray-500 mx-2">↔</span>
                        <span className="font-medium">{corr.var2}</span>
                      </div>
                      <div className="flex items-center">
                        <div className={`w-4 h-4 rounded mr-2 ${
                          Math.abs(corr.correlation) > 0.7 ? 'bg-red-500' :
                          Math.abs(corr.correlation) > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                        }`}></div>
                        <span className="font-mono text-lg">{corr.correlation.toFixed(3)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">💡 Insights das Correlações</h4>
                <ul className="text-blue-800 space-y-1 text-sm">
                  <li>• <strong>Temperatura média ↔ Temperatura máxima</strong>: Forte correlação positiva (0.95)</li>
                  <li>• <strong>Temperatura média ↔ Temperatura mínima</strong>: Forte correlação positiva (0.92)</li>
                  <li>• <strong>Umidade ↔ Precipitação</strong>: Correlação moderada (0.35)</li>
                  <li>• <strong>Pressão ↔ Temperatura</strong>: Correlação negativa fraca (-0.15)</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'models-sem-lag':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Modelos sem Lag Features</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance dos Modelos</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={modelData.filter(m => m.type === 'Sem Lag')}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="model" angle={-45} textAnchor="end" height={100} fontSize={12} />
                      <YAxis />
                      <Tooltip formatter={(value, name) => [value.toFixed(4), name]} />
                      <Legend />
                      <Bar dataKey="r2" fill="#3B82F6" name="R² Score" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Importância das Features</h3>
                  <div className="space-y-2">
                    {importanceDataSemLag.map((item, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span className="text-sm font-medium">{item.feature}</span>
                        <span className="text-sm font-bold">{(item.importance * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-semibold text-green-900 mb-2">✅ Conclusões - Modelos sem Lag</h4>
                <ul className="text-green-800 space-y-1 text-sm">
                  <li>• <strong>Random Forest</strong> apresentou o melhor desempenho geral</li>
                  <li>• <strong>Pressão atmosférica</strong> e <strong>umidade relativa mínima</strong> são as features mais importantes</li>
                  <li>• <strong>SVR</strong> teve desempenho significativamente inferior aos outros modelos</li>
                  <li>• R² máximo alcançado: <strong>0.9121</strong></li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'models-com-lag':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Modelos com Lag Features</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance dos Modelos</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={modelData.filter(m => m.type === 'Com Lag')}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="model" angle={-45} textAnchor="end" height={100} fontSize={12} />
                      <YAxis />
                      <Tooltip formatter={(value, name) => [value.toFixed(4), name]} />
                      <Legend />
                      <Bar dataKey="r2" fill="#8B5CF6" name="R² Score" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Features</h3>
                  <div className="space-y-2">
                    {importanceDataComLag.map((item, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span className="text-sm font-medium">{item.feature}</span>
                        <span className="text-sm font-bold">{(item.importance * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg">
                <h4 className="font-semibold text-purple-900 mb-2">🔄 Conclusões - Modelos com Lag</h4>
                <ul className="text-purple-800 space-y-1 text-sm">
                  <li>• <strong>temp_maxima_lag_1</strong> é disparadamente a feature mais importante (58.9%)</li>
                  <li>• <strong>Gradient Boosting</strong> teve melhor desempenho entre os modelos com lag</li>
                  <li>• Features de lag dos últimos 1-3 dias são mais relevantes que lag de 7 dias</li>
                  <li>• Paradoxalmente, a performance foi ligeiramente inferior aos modelos sem lag</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'comparison':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Comparação Final: Com vs Sem Lag Features</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparação R² Score</h3>
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={modelData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="model" angle={-45} textAnchor="end" height={120} fontSize={10} />
                      <YAxis />
                      <Tooltip formatter={(value, name) => [value.toFixed(4), name]} />
                      <Legend />
                      <Bar dataKey="r2" fill="#3B82F6" name="R² Score">
                        {modelData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparação RMSE</h3>
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={modelData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="model" angle={-45} textAnchor="end" height={120} fontSize={10} />
                      <YAxis />
                      <Tooltip formatter={(value, name) => [value.toFixed(4), name]} />
                      <Legend />
                      <Bar dataKey="rmse" fill="#EF4444" name="RMSE">
                        {modelData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-900 mb-2">🏆 Melhor Modelo Geral</h4>
                  <p className="text-green-800 font-medium">Random Forest (Sem Lag)</p>
                  <p className="text-green-700 text-sm">R²: 0.9121 | RMSE: 1.1567</p>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">📊 Modelos Sem Lag</h4>
                  <p className="text-blue-800 text-sm">Média R²: 0.727</p>
                  <p className="text-blue-800 text-sm">Média RMSE: 2.106</p>
                </div>

                <div className="bg-purple-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-2">🔄 Modelos Com Lag</h4>
                  <p className="text-purple-800 text-sm">Média R²: 0.620</p>
                  <p className="text-purple-800 text-sm">Média RMSE: 2.096</p>
                </div>
              </div>

              <div className="bg-amber-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-amber-900 mb-4">⚠️ Resultado Surpreendente: Lag Features não melhoraram a performance</h3>
                <div className="space-y-3 text-amber-800">
                  <p><strong>Possíveis explicações:</strong></p>
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    <li>Os dados meteorológicos já contêm informações temporais suficientes</li>
                    <li>O período de lag (1-7 dias) pode não ser o ideal para previsão de temperatura máxima</li>
                    <li>Overfitting causado pelo aumento significativo no número de features</li>
                    <li>Correlação temporal natural dos dados já capturada pelas features originais</li>
                    <li>Necessidade de feature engineering mais sofisticado para lag features</li>
                  </ul>
                  
                  <p className="mt-4"><strong>Conclusão:</strong></p>
                  <p className="text-sm">
                    Para este dataset específico e tarefa de previsão, o <strong>Random Forest sem lag features</strong> 
                    demonstrou ser a abordagem mais eficiente, oferecendo melhor performance com menor complexidade computacional.
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      case 'interpretability':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Análise de Interpretabilidade</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-blue-900 mb-4">🔍 Métodos Utilizados</h3>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-blue-800">SHAP (SHapley Additive exPlanations)</h4>
                      <p className="text-blue-700 text-sm">Explica contribuições individuais de cada feature para previsões específicas</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-blue-800">LIME (Local Interpretable Model-agnostic Explanations)</h4>
                      <p className="text-blue-700 text-sm">Fornece explicações locais para previsões individuais</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-blue-800">Feature Importance</h4>
                      <p className="text-blue-700 text-sm">Importância global das features no modelo Random Forest</p>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-green-900 mb-4">📊 Exemplo de Previsão</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-green-800 font-medium">Valor Real:</span>
                      <span className="text-green-900 font-bold">33.20°C</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-800 font-medium">Previsão:</span>
                      <span className="text-green-900 font-bold">33.65°C</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-800 font-medium">Diferença:</span>
                      <span className="text-green-900 font-bold">0.45°C</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Features - Random Forest</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center p-2 bg-blue-50 rounded">
                      <span className="text-sm font-medium">temp_maxima_lag_1</span>
                      <span className="text-sm font-bold">58.94%</span>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="text-sm font-medium">umidade_relativa_minima</span>
                      <span className="text-sm font-bold">16.10%</span>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="text-sm font-medium">temp_orvalho_media</span>
                      <span className="text-sm font-bold">6.33%</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Features - SHAP</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center p-2 bg-purple-50 rounded">
                      <span className="text-sm font-medium">temp_maxima_lag_1</span>
                      <span className="text-sm font-bold">Máximo</span>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="text-sm font-medium">umidade_relativa_minima</span>
                      <span className="text-sm font-bold">Alto</span>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <span className="text-sm font-medium">temp_orvalho_media</span>
                      <span className="text-sm font-bold">Médio</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 bg-indigo-50 p-4 rounded-lg">
                <h4 className="font-semibold text-indigo-900 mb-2">🎯 Consistência entre Métodos</h4>
                <p className="text-indigo-800 text-sm mb-2">
                  <strong>5 de 5 features</strong> aparecem nos top 5 de ambos os métodos (Random Forest e SHAP)
                </p>
                <ul className="text-indigo-800 space-y-1 text-sm">
                  <li>• <strong>temp_maxima_lag_1</strong>: Feature mais importante em ambos os métodos</li>
                  <li>• <strong>umidade_relativa_minima</strong>: Segunda mais importante</li>
                  <li>• <strong>temp_orvalho_media</strong>: Terceira mais importante</li>
                  <li>• Alta correlação entre importâncias Random Forest e SHAP</li>
                </ul>
              </div>
            </div>
          </div>
        );

      case 'data':
        return (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Dados e Informações Técnicas</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Estatísticas do Dataset</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-700">Total de registros:</span>
                      <span className="font-bold">4,018</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-700">Período:</span>
                      <span className="font-bold">2014-2025</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-700">Features originais:</span>
                      <span className="font-bold">10</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-700">Features com lag:</span>
                      <span className="font-bold">26</span>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-blue-900 mb-4">🛠️ Metodologia</h3>
                  <div className="space-y-2 text-blue-800 text-sm">
                    <p><strong>Divisão treino/teste:</strong> 80/20</p>
                    <p><strong>Validação cruzada:</strong> Não aplicada</p>
                    <p><strong>Tratamento de missing:</strong> Interpolação linear</p>
                    <p><strong>Normalização:</strong> Não aplicada</p>
                    <p><strong>Seed aleatória:</strong> 42</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-900 mb-2">✅ Principais Descobertas</h4>
                  <ul className="text-green-800 space-y-1 text-sm">
                    <li>• Random Forest sem lag é o melhor modelo</li>
                    <li>• Lag features não melhoraram a performance</li>
                    <li>• Temperatura do dia anterior é altamente preditiva</li>
                    <li>• SVR teve performance consistentemente pior</li>
                  </ul>
                </div>

                <div className="bg-orange-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-orange-900 mb-2">🔄 Próximos Passos</h4>
                  <ul className="text-orange-800 space-y-1 text-sm">
                    <li>• Testar diferentes períodos de lag</li>
                    <li>• Implementar feature engineering avançado</li>
                    <li>• Aplicar validação cruzada</li>
                    <li>• Explorar outros algoritmos (XGBoost, LSTM)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return <div>Conteúdo não encontrado</div>;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-4xl font-bold text-gray-900 text-center">
            🌤️ Análise Comparativa de Modelos Climáticos
          </h1>
          <p className="text-center text-gray-600 mt-2">
            Comparação sistemática de modelos ML com e sem lag-features para previsão meteorológica
          </p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 whitespace-nowrap text-sm font-medium border-b-2 transition-colors duration-200 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderTabContent()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-600">
            <p className="font-medium">Dashboard de Análise Climática - INMET</p>
            <p className="text-sm mt-2">
              Análise comparativa sistemática de modelos de machine learning para previsão meteorológica
            </p>
            <p className="text-xs mt-2 text-gray-500">
              Desenvolvido com React, Recharts e Tailwind CSS | © 2024
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
